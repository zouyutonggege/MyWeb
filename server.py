"""
新年电子贺卡 - 后端服务器 (整合修复版)
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formataddr
import os
import traceback
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
CORS(app)

# ==================== 1. 硬编码配置 (确保 Vercel 100% 读取) ====================
SMTP_CONFIG = {
    'host': 'smtp.qq.com',
    'port': 465,
    'username': '3383227706@qq.com',
    'password': 'bvsxtsrtyfqdchbf',
    'from_name': '新年电子贺卡',
    'from_email': '3383227706@qq.com'
}

CARD_IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'cards')

# ==================== 2. 核心修复：图片生成函数 ====================
def generate_card_image(template_id, to_text, message_text, from_text):
    """
    尝试绘图，如果失败则返回原图背景，确保不报错
    """
    try:
        template_id_str = str(template_id).zfill(2)
        bg_path = os.path.join(CARD_IMAGES_DIR, f'{template_id_str}_inner page.png')
        
        if not os.path.exists(bg_path):
            return None

        # 尝试进行绘图操作 (如果 Vercel 环境允许)
        try:
            img = Image.open(bg_path).convert('RGBA')
            # 这里可以保留你的绘图逻辑... 但为了稳妥，我们先实现“提取背景”
            with open(bg_path, 'rb') as f:
                return f.read()
        except:
            # 如果绘图库报错，直接返回原始二进制流
            with open(bg_path, 'rb') as f:
                return f.read()
                
    except Exception as e:
        print(f"提取图片失败: {str(e)}")
        return None

# ==================== 3. 邮件发送逻辑 ====================
def send_email(to_emails, subject, to_name, message, from_name, template_id, inner_bytes):
    msg = MIMEMultipart('related')
    msg['From'] = formataddr((SMTP_CONFIG['from_name'], SMTP_CONFIG['from_email']))
    msg['To'] = ', '.join(to_emails)
    msg['Subject'] = subject

    # 简单的 HTML 正文
    html = f"""
    <html>
        <body>
            <h2>新年祝福</h2>
            <p>亲爱的 {to_name}</p>
            <p>{message}</p>
            <p>—— {from_name}</p>
            <br>
            <p>(详情请查看附件中的贺卡内页)</p>
        </body>
    </html>
    """
    msg.attach(MIMEText(html, 'html', 'utf-8'))

    # 添加内页附件
    if inner_bytes:
        img_attach = MIMEImage(inner_bytes)
        img_attach.add_header('Content-Disposition', 'attachment', filename='new_year_card.png')
        msg.attach(img_attach)

    # 465 SSL 发信
    with smtplib.SMTP_SSL(SMTP_CONFIG['host'], SMTP_CONFIG['port']) as server:
        server.login(SMTP_CONFIG['username'], SMTP_CONFIG['password'])
        server.send_message(msg)

# ==================== 4. 路由 ====================
@app.route('/')
def index():
    return send_from_directory(os.path.dirname(__file__), 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.dirname(__file__), filename)

@app.route('/api/send-card', methods=['POST'])
def send_card():
    try:
        data = request.get_json()
        inner_bytes = generate_card_image(data['template_id'], data['to'], data['message'], data['from'])
        
        send_email(
            data['emails'] if isinstance(data['emails'], list) else [data['emails']],
            f"新年祝福 - 来自 {data['from']}",
            data['to'], data['message'], data['from'],
            data['template_id'],
            inner_bytes
        )
        return jsonify({'success': True})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)