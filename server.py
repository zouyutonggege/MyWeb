"""
新年电子贺卡 - 后端服务器
提供邮件发送功能
使用PIL动态生成贺卡内页图片，精确复刻前端CSS布局
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formataddr
import os
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import traceback
from jinja2 import Template
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

app = Flask(__name__)
CORS(app)

# ==================== 配置 ====================
# 邮件服务器配置 (请根据实际情况修改)
SMTP_CONFIG = {
    'host': 'smtp.qq.com',
    'port': 465,
    'use_tls': True,   # 把 False 改成 True
    'username': '3383227706@qq.com',                # 直接写你的 QQ 号
    'password': 'bvsxtsrtyfqdchbf',                # 直接写你的授权码
    'from_name': '新年电子贺卡',                     
    'from_email': '3383227706@qq.com'               # 直接写你的发件邮箱
}

# 贺卡图片路径
CARD_IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'cards')
# 邮件模板路径
EMAIL_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates', 'email_template.html')

# ==================== 辅助函数 ====================

def validate_email(email):
    """验证邮箱格式"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def get_font(size, bold=False):
    """
    获取中文字体，优先使用楷体
    
    Args:
        size: 字体大小
        bold: 是否加粗
        
    Returns:
        ImageFont对象
    """
    font_paths = [
        # Windows 字体路径 - 楷体优先
        r'C:\Windows\Fonts\simkai.ttf',       # 楷体
        r'C:\Windows\Fonts\STKAITI.TTF',      # 华文楷体
        r'C:\Windows\Fonts\msyh.ttc',         # 微软雅黑
        r'C:\Windows\Fonts\msyhbd.ttc',       # 微软雅黑粗体
        r'C:\Windows\Fonts\simhei.ttf',       # 黑体
        r'C:\Windows\Fonts\simsun.ttc',       # 宋体
        # Linux 字体路径
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
        '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/arphic/ukai.ttc',  # AR PL UKai (楷体)
        # macOS 字体路径
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/STHeiti Medium.ttc',
        '/Library/Fonts/Kaiti.ttc',  # 楷体
    ]

    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                font = ImageFont.truetype(font_path, size)
                print(f"✓ 使用字体: {font_path}, 大小: {size}px")
                return font
            except Exception as e:
                print(f"✗ 加载字体失败 {font_path}: {str(e)}")
                continue
    
    # 如果没有找到字体，使用默认字体
    print(f"⚠ 未找到中文字体，使用默认字体")
    return ImageFont.load_default()

def wrap_text(text, font, max_width, draw):
    """
    自动换行文本
    
    Args:
        text: 要换行的文本
        font: 字体对象
        max_width: 最大宽度（像素）
        draw: ImageDraw对象
        
    Returns:
        换行后的文本列表
    """
    lines = []
    
    # 处理已有的换行符
    paragraphs = text.replace('\\n', '\n').split('\n')
    
    for paragraph in paragraphs:
        if not paragraph.strip():
            lines.append('')
            continue
        
        current_line = ''
        
        for char in paragraph:
            test_line = current_line + char
            bbox = draw.textbbox((0, 0), test_line, font=font)
            width = bbox[2] - bbox[0]
            
            if width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = char
        
        if current_line:
            lines.append(current_line)
    
    return lines

def draw_text_simple(draw, position, text, font, text_color):
    """
    绘制纯文字（无阴影）
    
    Args:
        draw: ImageDraw对象
        position: 文字位置 (x, y)
        text: 文字内容
        font: 字体对象
        text_color: 文字颜色
    """
    draw.text(position, text, font=font, fill=text_color)

def generate_card_image(template_id, to_text, message_text, from_text):
    """
    生成贺卡内页图片，精确复刻前端CSS布局
    
    前端CSS布局分析：
    - .card-text-overlay: position absolute, inset 0, 背景透明
    - .text-group: flex column, justify-content center, align-items flex-start
    - gap: --spacing-md (24px) -> 实际使用30px
    - .text-to: 左对齐，字体大，颜色 #d45230
    - .text-message: 居中对齐，字体最大，颜色 #333，动态大小
    - .text-from: 右对齐，字体中，颜色 #666
    
    Args:
        template_id: 模板ID (1-6)
        to_text: 收件人姓名（例如："亲爱的你"）
        message_text: 祝福语（支持\n换行）
        from_text: 发件人署名（例如："来自远方"）
        
    Returns:
        图片字节流（PNG格式）
    """
    try:
        print(f"\n========== 开始生成贺卡图片 ==========")
        print(f"模板ID: {template_id}")
        print(f"致: {to_text}")
        print(f"祝福语: {message_text[:50]}...")
        print(f"署名: {from_text}")
        
        # 1. 读取背景图
        template_id_str = str(template_id).zfill(2)
        bg_path = os.path.join(CARD_IMAGES_DIR, f'{template_id_str}_inner page.png')
        
        if not os.path.exists(bg_path):
            print(f"✗ 背景图不存在: {bg_path}")
            # 创建一个简单的占位图
            img = Image.new('RGB', (800, 1000), color=(248, 216, 157))
            draw = ImageDraw.Draw(img)
            draw.rectangle([(0, 0), (800, 1000)], outline=(212, 82, 48), width=10)
        else:
            print(f"✓ 加载背景图: {bg_path}")
            img = Image.open(bg_path).convert('RGBA')
        
        width, height = img.size
        print(f"✓ 图片尺寸: {width}x{height}")
        
        # 创建绘图对象
        draw = ImageDraw.Draw(img, 'RGBA')
        
        # 2. 字体设置（参考CSS）
        # CSS font-size: 
        # - .text-to: 约 2rem = 32px
        # - .text-message: 动态，默认 2rem，最小 0.95rem = 15px
        # - .text-from: 约 1rem = 16px
        
        to_font_size = int(width * 0.045)  # 约占图片宽度4.5%
        from_font_size = int(width * 0.028)  # 约占图片宽度2.8%
        
        # 根据祝福语长度动态调整字体大小（复刻前端逻辑）
        message_length = len(message_text)
        if message_length <= 20:
            message_font_size = int(width * 0.075)  # 最大
        elif message_length <= 40:
            message_font_size = int(width * 0.065)
        elif message_length <= 60:
            message_font_size = int(width * 0.058)
        elif message_length <= 80:
            message_font_size = int(width * 0.050)
        elif message_length <= 100:
            message_font_size = int(width * 0.045)
        elif message_length <= 120:
            message_font_size = int(width * 0.040)
        else:
            message_font_size = int(width * 0.037)  # 最小
        
        print(f"✓ 字体大小: 致={to_font_size}px, 祝福语={message_font_size}px, 署名={from_font_size}px")
        
        to_font = get_font(to_font_size)
        message_font = get_font(message_font_size)
        from_font = get_font(from_font_size)
        
        # 3. 颜色定义（参考CSS）
        color_primary = (212, 82, 48)      # #d45230
        color_text_dark = (51, 51, 51)     # #333
        color_text_gray = (102, 102, 102)  # #666
        
        # 4. 计算文字尺寸和位置
        
        # === 致 (To) ===
        to_bbox = draw.textbbox((0, 0), to_text, font=to_font)
        to_text_width = to_bbox[2] - to_bbox[0]
        to_text_height = to_bbox[3] - to_bbox[1]
        
        # === 祝福语 (Message) - 支持多行 ===
        max_message_width = int(width * 0.85)  # 最大宽度85%
        message_lines = wrap_text(message_text, message_font, max_message_width, draw)
        
        # 计算祝福语总高度（行高 = 字体大小 * 1.6）
        line_height = int(message_font_size * 1.6)
        message_total_height = len(message_lines) * line_height
        
        # 计算每行的宽度（用于居中）
        message_line_widths = []
        for line in message_lines:
            bbox = draw.textbbox((0, 0), line, font=message_font)
            message_line_widths.append(bbox[2] - bbox[0])
        
        # === 署名 (From) ===
        from_bbox = draw.textbbox((0, 0), from_text, font=from_font)
        from_text_width = from_bbox[2] - from_bbox[0]
        from_text_height = from_bbox[3] - from_bbox[1]
        
        # 5. 计算整体组的垂直居中位置
        # CSS: .text-group { display: flex; flex-direction: column; justify-content: center; gap: 30px }
        
        gap = int(height * 0.03)  # 间距约为高度的3%（约30px）
        
        # 整体组的总高度
        total_group_height = to_text_height + gap + message_total_height + gap + from_text_height
        
        # 整体组的起始Y坐标（垂直居中）
        group_start_y = (height - total_group_height) // 2
        
        print(f"✓ 整体组高度: {total_group_height}px")
        print(f"✓ 整体组起始Y: {group_start_y}px")
        print(f"✓ 祝福语行数: {len(message_lines)}")
        
        # 6. 绘制文字
        
        # === 绘制"致" (左对齐，左边距10%) ===
        to_x = int(width * 0.10)
        to_y = group_start_y
        
        print(f"✓ 绘制'致': 位置({to_x}, {to_y})")
        draw_text_simple(
            draw, 
            (to_x, to_y), 
            to_text, 
            to_font, 
            color_primary
        )
        
        # === 绘制祝福语 (水平居中，每行单独居中) ===
        message_y = to_y + to_text_height + gap
        
        print(f"✓ 绘制祝福语: 起始Y={message_y}")
        for i, line in enumerate(message_lines):
            if not line.strip():
                continue
            
            # 每行单独居中
            line_x = (width - message_line_widths[i]) // 2
            line_y = message_y + i * line_height
            
            draw_text_simple(
                draw,
                (line_x, line_y),
                line,
                message_font,
                color_text_dark
            )
        
        # === 绘制署名 (右对齐，右边距10%) ===
        from_x = int(width * 0.90) - from_text_width
        from_y = message_y + message_total_height + gap
        
        print(f"✓ 绘制'署名': 位置({from_x}, {from_y})")
        draw_text_simple(
            draw,
            (from_x, from_y),
            from_text,
            from_font,
            color_text_gray
        )
        
        # 7. 保存为字节流
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG', quality=95)
        img_byte_arr.seek(0)
        img_bytes = img_byte_arr.getvalue()
        
        print(f"✓ 图片生成成功，大小: {len(img_bytes)} bytes")
        print(f"========== 贺卡图片生成完成 ==========\n")
        
        return img_bytes
        
    except Exception as e:
        print(f"✗ 生成贺卡图片失败: {str(e)}")
        traceback.print_exc()
        return None

def load_email_template():
    """
    加载邮件HTML模板
    
    Returns:
        Jinja2 Template对象
    """
    try:
        with open(EMAIL_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            template_content = f.read()
        return Template(template_content)
    except Exception as e:
        print(f"加载邮件模板失败: {str(e)}")
        # 返回一个简单的后备模板
        fallback_template = """
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"></head>
        <body>
            <h2>新年祝福</h2>
            <p>亲爱的 {{ to_name }}</p>
            <p>{{ message }}</p>
            <p>—— {{ from_name }}</p>
        </body>
        </html>
        """
        return Template(fallback_template)

def generate_html_email(to_name, message, from_name):
    """
    生成HTML邮件内容

    Args:
        to_name: 收件人姓名
        message: 祝福语
        from_name: 发件人姓名

    Returns:
        HTML字符串
    """
    template = load_email_template()
    return template.render(
        to_name=to_name,
        message=message,
        from_name=from_name
    )

def send_email(to_emails, subject, html_content, cover_gif_path, cover_png_path, inner_card_bytes):
    """
    发送邮件
    - 封面GIF在正文中显示（Content-ID）
    - 封面PNG和内页图作为普通附件

    Args:
        to_emails: 收件人邮箱列表
        subject: 邮件主题
        html_content: HTML内容
        cover_gif_path: 封面GIF文件路径（用于正文显示）
        cover_png_path: 封面PNG文件路径（作为附件）
        inner_card_bytes: 内页合成图字节流（作为附件）
    """
    if not SMTP_CONFIG['username'] or not SMTP_CONFIG['password']:
        raise ValueError('SMTP配置不完整，请设置SMTP_USERNAME和SMTP_PASSWORD环境变量')

    print(f"\n========== 开始发送邮件 ==========")
    print(f"收件人: {to_emails}")
    print(f"主题: {subject}")
    
    # 创建邮件对象
    msg = MIMEMultipart('related')
    msg['From'] = formataddr((SMTP_CONFIG['from_name'], SMTP_CONFIG['from_email']))
    msg['To'] = ', '.join(to_emails)
    msg['Subject'] = subject

    # 添加HTML内容
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))
    print(f"✓ HTML内容已添加")

    # 1. 添加封面GIF（用于正文显示，使用Content-ID）
    if cover_gif_path and os.path.exists(cover_gif_path):
        with open(cover_gif_path, 'rb') as f:
            cover_gif_data = f.read()
        
        cover_gif_inline = MIMEImage(cover_gif_data, _subtype='gif')
        cover_gif_inline.add_header('Content-ID', '<cover_gif>')
        cover_gif_inline.add_header('Content-Disposition', 'inline', filename='cover.gif')
        msg.attach(cover_gif_inline)
        print(f"✓ 封面GIF已添加（正文显示）: {len(cover_gif_data)} bytes")
    else:
        print(f"✗ 封面GIF不存在: {cover_gif_path}")

    # 2. 添加封面PNG（作为普通附件）
    if cover_png_path and os.path.exists(cover_png_path):
        with open(cover_png_path, 'rb') as f:
            cover_png_data = f.read()
        
        cover_png_attachment = MIMEImage(cover_png_data)
        cover_png_attachment.add_header('Content-Disposition', 'attachment', filename='cover.png')
        msg.attach(cover_png_attachment)
        print(f"✓ 封面PNG已添加（附件）: {len(cover_png_data)} bytes")
    else:
        print(f"✗ 封面PNG不存在: {cover_png_path}")

    # 3. 添加内页合成图（作为普通附件）
    if inner_card_bytes:
        inner_card_attachment = MIMEImage(inner_card_bytes)
        inner_card_attachment.add_header('Content-Disposition', 'attachment', filename='new_year_card.png')
        msg.attach(inner_card_attachment)
        print(f"✓ 内页图片已添加（附件）: {len(inner_card_bytes)} bytes")
    else:
        print(f"✗ 内页图片数据为空")

    # 发送邮件
    print(f"正在连接SMTP服务器...")
    with smtplib.SMTP(SMTP_CONFIG['host'], SMTP_CONFIG['port']) as server:
        if SMTP_CONFIG['use_tls']:
            server.starttls()
            print(f"✓ TLS连接已建立")
        server.login(SMTP_CONFIG['username'], SMTP_CONFIG['password'])
        print(f"✓ SMTP登录成功")
        server.send_message(msg)
        print(f"✓ 邮件发送成功！")
        print(f"========== 邮件发送完成 ==========\n")

# ==================== 路由 ====================

@app.route('/')
def index():
    """首页 - 返回前端页面"""
    return send_from_directory(os.path.dirname(__file__), 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    """静态文件服务"""
    return send_from_directory(os.path.dirname(__file__), filename)

@app.route('/api/send-card', methods=['POST'])
def send_card():
    """
    发送贺卡邮件

    请求参数 (JSON):
        template_id: 模板ID (1-6)
        to: 收件人姓名
        message: 祝福语
        from: 发件人姓名
        emails: 收件人邮箱列表 (字符串数组)
        card_preview_base64: (忽略) 前端传来的截图，不再使用
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'error': '请求数据为空'}), 400

        # 验证必填字段
        required_fields = ['template_id', 'to', 'message', 'from', 'emails']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'success': False, 'error': f'缺少必填字段: {field}'}), 400

        template_id = data['template_id']
        to_name = data['to']
        message = data['message']
        from_name = data['from']
        emails = data['emails']
        
        # 忽略前端传来的 card_preview_base64
        if 'card_preview_base64' in data:
            print(f"ℹ 收到前端base64图片，但将使用后端PIL生成")

        # 验证邮箱
        if not isinstance(emails, list):
            emails = [emails]

        valid_emails = [e for e in emails if validate_email(e)]
        if not valid_emails:
            return jsonify({'success': False, 'error': '没有有效的邮箱地址'}), 400

        invalid_emails = set(emails) - set(valid_emails)
        if invalid_emails:
            return jsonify({
                'success': False,
                'error': f'无效的邮箱地址: {", ".join(invalid_emails)}'
            }), 400

        # 生成邮件内容
        subject = f'新年祝福 - 来自 {from_name} 的贺卡'
        html_content = generate_html_email(to_name, message, from_name)

        # 获取文件路径
        template_id_str = str(template_id).zfill(2)
        cover_gif_path = os.path.join(CARD_IMAGES_DIR, f'{template_id_str}_cover.gif')
        cover_png_path = os.path.join(CARD_IMAGES_DIR, f'{template_id_str}_cover.png')

        # 使用PIL生成内页图片
        print(f"\n" + "="*60)
        print(f"开始处理贺卡发送请求")
        print(f"="*60)
        
        inner_card_bytes = generate_card_image(
            template_id=template_id,
            to_text=to_name,
            message_text=message,
            from_text=from_name
        )
        
        if not inner_card_bytes:
            return jsonify({
                'success': False,
                'error': '生成贺卡图片失败'
            }), 500

        # 发送邮件
        send_email(valid_emails, subject, html_content, cover_gif_path, cover_png_path, inner_card_bytes)

        return jsonify({
            'success': True,
            'message': f'已成功发送至 {len(valid_emails)} 个邮箱',
            'sent_count': len(valid_emails)
        })

    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except smtplib.SMTPAuthenticationError:
        return jsonify({
            'success': False,
            'error': 'SMTP认证失败，请检查邮箱和授权码配置'
        }), 500
    except Exception as e:
        print(f"发送邮件失败: {str(e)}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': f'发送失败: {str(e)}'}), 500

@app.route('/api/config', methods=['GET'])
def get_config():
    """获取当前SMTP配置状态（用于前端提示）"""
    has_config = bool(SMTP_CONFIG['username'] and SMTP_CONFIG['password'])
    return jsonify({
        'configured': has_config,
        'from_email': SMTP_CONFIG['from_email'] if has_config else ''
    })

# ==================== 启动 ====================

if __name__ == '__main__':
    print("=" * 60)
    print("新年电子贺卡 - 后端服务器 (PIL图片生成版)")
    print("=" * 60)
    print(f"服务地址: http://localhost:5000")
    print()

    if not SMTP_CONFIG['username'] or not SMTP_CONFIG['password']:
        print("⚠️  警告: SMTP配置不完整！")
        print("请设置以下环境变量:")
        print("  SMTP_USERNAME=你的邮箱")
        print("  SMTP_PASSWORD=邮箱密码/授权码")
        print("  SMTP_HOST=smtp服务器地址 (默认: smtp.qq.com)")
        print("  SMTP_PORT=端口号 (默认: 587)")
        print()
        print("常见邮箱SMTP配置:")
        print("  QQ邮箱: smtp.qq.com:587")
        print("  163邮箱: smtp.163.com:465")
        print("  Gmail: smtp.gmail.com:587")
        print()

    print("=" * 60)
    print("启动开发服务器...")
    print("=" * 60)

    # 启动服务器
    app.run(host='0.0.0.0', port=5000, debug=True)
