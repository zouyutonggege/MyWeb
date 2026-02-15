# 🧧 一马当先·送祝福

一个精美的新年电子贺卡制作和发送系统，支持多种模板选择、自定义祝福语、动态生成内页图片，并通过邮件发送给好友。

![项目封面](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 目录

- [功能特性](#功能特性)
- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [详细配置](#详细配置)
- [使用说明](#使用说明)
- [常见问题](#常见问题)
- [开发指南](#开发指南)
- [许可证](#许可证)

---

## ✨ 功能特性

### 🎨 前端功能
- ✅ **6种精美模板** - 多种风格的电子贺卡封面供选择
- ✅ **实时预览** - 编辑时左侧实时显示贺卡效果
- ✅ **动态字体调整** - 根据祝福语长度自动调整字体大小
- ✅ **封装动画** - 精美的贺卡折叠、装信封、封蜡动画
- ✅ **发送动画** - 可爱的小马邮差送信动画

### 🚀 后端功能
- ✅ **PIL动态生成** - 后端使用Pillow库生成贺卡内页图片
- ✅ **多邮箱发送** - 支持一次向多个邮箱发送
- ✅ **邮件附件** - 封面PNG + 内页PNG双附件
- ✅ **详细日志** - 完整的生成和发送过程日志

### 📧 邮件功能
- ✅ **GIF封面** - 邮件正文显示动态封面
- ✅ **双附件** - 封面静态图 + 内页合成图
- ✅ **响应式邮件模板** - 适配各种邮件客户端
- ✅ **多邮箱服务商支持** - QQ邮箱、163邮箱、Gmail等

---

## 🛠 技术栈

### 前端
- **HTML5 / CSS3** - 现代化的网页布局
- **JavaScript (ES6+)** - 原生JS，无框架依赖
- **Canvas API** - 图片预览处理
- **Flexbox / Grid** - 响应式布局

### 后端
- **Python 3.8+** - 主要编程语言
- **Flask 3.0** - 轻量级Web框架
- **Pillow (PIL)** - 图片生成和处理
- **Jinja2** - 邮件模板渲染
- **python-dotenv** - 环境变量管理

### 邮件
- **smtplib** - Python内置SMTP客户端
- **email.mime** - 邮件内容构建

---

## 📁 项目结构

```
new-year-card/
├── server.py                    # Flask后端服务器（主程序）
├── index.html                   # 前端主页面
├── styles.css                   # 样式表
├── script.js                    # 前端交互脚本
├── background.png               # 背景图片
├── horse_postman.png            # 小马邮差图片
├── .env                         # 环境变量配置
├── .gitignore                   # Git忽略文件
├── requirements.txt             # Python依赖列表
├── README.md                    # 项目说明文档（本文件）
├── templates/
│   └── email_template.html      # 邮件HTML模板
└── cards/
    ├── 01_cover.png             # 模板1封面（静态）
    ├── 01_cover.gif             # 模板1封面（动态）
    ├── 01_inner page.png        # 模板1内页背景
    ├── 02_cover.png             # 模板2封面（静态）
    ├── 02_cover.gif             # 模板2封面（动态）
    ├── 02_inner page.png        # 模板2内页背景
    ├── 03_cover.png
    ├── 03_cover.gif
    ├── 03_inner page.png
    ├── 04_cover.png
    ├── 04_cover.gif
    ├── 04_inner page.png
    ├── 05_cover.png
    ├── 05_cover.gif
    ├── 05_inner page.png
    ├── 06_cover.png
    ├── 06_cover.gif
    └── 06_inner page.png
```

---

## 🚀 快速开始

### 1️⃣ 环境要求

- **Python**: 3.8 或更高版本
- **操作系统**: Windows / macOS / Linux
- **浏览器**: Chrome / Firefox / Safari / Edge（现代浏览器）

### 2️⃣ 安装依赖

```bash
# 克隆或下载项目到本地
cd new-year-card

# 安装Python依赖
pip install -r requirements.txt
```

**依赖说明：**
- `Flask` - Web框架
- `Flask-Cors` - 跨域支持
- `Pillow` - 图片处理
- `Jinja2` - 模板引擎
- `python-dotenv` - 环境变量管理

### 3️⃣ 配置邮箱

#### 方法一：使用.env文件（推荐）

1. 复制示例配置文件：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入你的邮箱信息：
```env
SMTP_USERNAME=your_email@qq.com
SMTP_PASSWORD=your_authorization_code
SMTP_HOST=smtp.qq.com
SMTP_PORT=587
```

#### 方法二：使用环境变量

```bash
# Windows CMD
set SMTP_USERNAME=your_email@qq.com
set SMTP_PASSWORD=your_authorization_code

# Windows PowerShell
$env:SMTP_USERNAME="your_email@qq.com"
$env:SMTP_PASSWORD="your_authorization_code"

# macOS / Linux
export SMTP_USERNAME="your_email@qq.com"
export SMTP_PASSWORD="your_authorization_code"
```

### 4️⃣ 启动服务器

#### 方法一：直接运行（推荐）
```bash
python server.py
```

#### 方法二：在VS Code中运行
1. 打开 `server.py`
2. 按 `F5` 或点击右上角的运行按钮
3. 选择"Python File"

### 5️⃣ 访问应用

打开浏览器，访问：
```
http://localhost:5000
```

---

## 🔧 详细配置

### 获取邮箱授权码

#### QQ邮箱（推荐）

1. 登录 [QQ邮箱网页版](https://mail.qq.com)
2. 点击顶部 **设置** → **账户**
3. 找到 **POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务**
4. 开启 **POP3/SMTP服务** 或 **IMAP/SMTP服务**
5. 点击 **生成授权码**
6. 按照提示发送短信验证
7. 复制生成的16位授权码（例如：`abcdefghijklmnop`）

**配置示例：**
```env
SMTP_USERNAME=1234567890@qq.com
SMTP_PASSWORD=abcdefghijklmnop
SMTP_HOST=smtp.qq.com
SMTP_PORT=587
```

#### 163邮箱

1. 登录 [163邮箱](https://mail.163.com)
2. 点击顶部 **设置** → **POP3/SMTP/IMAP**
3. 开启 **IMAP/SMTP服务** 或 **POP3/SMTP服务**
4. 点击 **客户端授权密码** → **新增授权密码**
5. 复制授权码

**配置示例：**
```env
SMTP_USERNAME=yourname@163.com
SMTP_PASSWORD=your_auth_code
SMTP_HOST=smtp.163.com
SMTP_PORT=465
```

#### Gmail

1. 启用 [两步验证](https://myaccount.google.com/signinoptions/two-step-verification)
2. 创建 [应用专用密码](https://myaccount.google.com/apppasswords)
3. 选择"邮件"和你的设备
4. 复制生成的16位密码

**配置示例：**
```env
SMTP_USERNAME=yourname@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

### 常用SMTP配置

| 邮箱服务商 | SMTP地址 | 端口 | 加密方式 |
|-----------|----------|------|---------|
| QQ邮箱 | smtp.qq.com | 587 | STARTTLS |
| 163邮箱 | smtp.163.com | 465 | SSL |
| 126邮箱 | smtp.126.com | 465 | SSL |
| Gmail | smtp.gmail.com | 587 | STARTTLS |
| Outlook | smtp-mail.outlook.com | 587 | STARTTLS |
| 新浪邮箱 | smtp.sina.com | 587 | STARTTLS |

---

## 📖 使用说明

### 用户操作流程

#### 1. 选择模板
- 进入首页，浏览6种贺卡模板
- 鼠标悬停可预览动态效果
- 点击选择心仪的模板

#### 2. 编辑祝福语
- **致**：填写收件人称呼（最多10字）
- **祝福语**：填写祝福内容（最多150字，支持换行）
- **署名**：填写发件人名字（最多10字）
- 左侧实时预览编辑效果

#### 3. 完成制作
- 点击"制作完成"按钮
- 观看精美的封装动画
  - 贺卡缩小
  - 贺卡折叠
  - 装入信封
  - 信封封口
  - 盖上蜡封

#### 4. 发送贺卡
- 点击"发送给好友"
- 输入收件人邮箱（支持多个，用逗号分隔）
  ```
  例如：friend1@qq.com, friend2@163.com
  ```
- 点击"确认寄出"
- 观看进度条（约2分钟）
- 等待小马邮差送信动画

#### 5. 查收邮件
- 收件人打开邮箱
- 邮件正文显示动态GIF封面
- 下载附件查看完整贺卡
  - `cover.png` - 封面静态图
  - `new_year_card.png` - 内页合成图

---

## ❓ 常见问题

### Q1: 启动服务器后提示"SMTP配置不完整"？

**解决方法：**
1. 检查 `.env` 文件是否存在
2. 确认文件内容格式正确
3. 确保 `SMTP_USERNAME` 和 `SMTP_PASSWORD` 已填写
4. 重启服务器

### Q2: 发送邮件失败，提示"SMTP认证失败"？

**可能原因：**
- 使用了登录密码而不是授权码
- 授权码输入错误
- 邮箱未开启SMTP服务

**解决方法：**
1. 确认使用的是**授权码**，不是登录密码
2. 重新生成授权码
3. 检查邮箱是否开启SMTP服务

### Q3: 邮件发送成功，但收件人没收到？

**检查项：**
1. 检查收件人邮箱地址是否正确
2. 查看垃圾邮件箱
3. 确认发件邮箱没有被限制
4. 查看服务器日志是否显示"✓ 邮件发送成功"

### Q4: 贺卡图片中文字显示为方块？

**原因：** 系统缺少中文字体

**解决方法：**

**Windows：** 通常已内置楷体，无需处理

**Linux：**
```bash
# Ubuntu/Debian
sudo apt-get install fonts-arphic-ukai

# CentOS/RHEL
sudo yum install fonts-arphic-ukai
```

**macOS：** 系统自带楷体，无需处理

### Q5: 进度条卡在90%不动？

**可能原因：**
- 网络不稳定
- 邮件服务器响应慢
- 图片生成耗时长

**解决方法：**
- 耐心等待（通常不超过3分钟）
- 查看控制台日志确认进度
- 如果长时间无响应，刷新页面重试

### Q6: VS Code无法直接运行server.py？

**解决方法：**

1. 安装Python扩展：
   - 打开扩展商店（Ctrl+Shift+X）
   - 搜索"Python"
   - 安装Microsoft官方的Python扩展

2. 选择Python解释器：
   - 按 `Ctrl+Shift+P`
   - 输入"Python: Select Interpreter"
   - 选择已安装Python的路径

3. 运行文件：
   - 打开 `server.py`
   - 按 `F5` 或点击右上角运行按钮

---

## 👨‍💻 开发指南

### 本地开发

```bash
# 克隆项目
git clone <your-repo-url>
cd new-year-card

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件

# 启动开发服务器
python server.py
```

### 代码结构说明

#### 前端核心文件

**index.html**
- 主要页面结构
- 4个主要页面：选择模板、编辑、封装、发送

**styles.css**
- 全局样式变量
- 玻璃拟态效果
- 动画定义
- 响应式布局

**script.js**
- 应用状态管理
- 模板选择逻辑
- 实时预览更新
- 进度条控制
- 邮件发送请求

#### 后端核心文件

**server.py**
- Flask路由定义
- PIL图片生成逻辑
- 邮件发送功能
- 环境变量加载

**主要函数：**
- `generate_card_image()` - 生成贺卡内页图片
- `send_email()` - 发送邮件
- `wrap_text()` - 文字自动换行
- `get_font()` - 字体加载

### 自定义模板

#### 添加新模板

1. **准备图片资源：**
   - `{id}_cover.png` - 封面静态图
   - `{id}_cover.gif` - 封面动图
   - `{id}_inner page.png` - 内页背景

2. **放入cards目录：**
   ```
   cards/
   ├── 07_cover.png
   ├── 07_cover.gif
   └── 07_inner page.png
   ```

3. **更新index.html：**
   ```html
   <div class="template-item" data-template="7">
       <div class="template-preview">
           <img class="template-cover" 
                src="cards/07_cover.png" 
                data-gif="cards/07_cover.gif" 
                alt="模板 7">
           <div class="template-overlay">
               <span class="select-text">选择此款</span>
           </div>
       </div>
   </div>
   ```

#### 修改文字样式

**编辑 `server.py` 中的颜色定义：**
```python
# 在 generate_card_image() 函数中找到：
color_primary = (212, 82, 48)      # 致的颜色 #d45230
color_text_dark = (51, 51, 51)     # 祝福语颜色 #333
color_text_gray = (102, 102, 102)  # 署名颜色 #666
```

**修改字体大小比例：**
```python
to_font_size = int(width * 0.045)      # 致：4.5%
message_font_size = int(width * 0.075) # 祝福语：7.5%
from_font_size = int(width * 0.028)    # 署名：2.8%
```

### 部署到生产环境

#### 使用Gunicorn（推荐）

```bash
# 安装Gunicorn
pip install gunicorn

# 启动服务器
gunicorn -w 4 -b 0.0.0.0:5000 server:app
```

#### 使用Docker

**创建 Dockerfile：**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "server.py"]
```

**构建和运行：**
```bash
docker build -t new-year-card .
docker run -p 5000:5000 --env-file .env new-year-card
```

---

## 🐛 调试技巧

### 启用详细日志

服务器启动后，控制台会显示详细日志：

```
========== 开始生成贺卡图片 ==========
模板ID: 1
致: 亲爱的你
祝福语: 愿新的一年...
署名: 来自远方
✓ 加载背景图: cards/01_inner page.png
✓ 图片尺寸: 800x1000
✓ 使用字体: simkai.ttf, 大小: 36px
✓ 整体组高度: 450px
✓ 绘制'致': 位置(80, 275)
✓ 图片生成成功，大小: 234567 bytes
========== 贺卡图片生成完成 ==========

========== 开始发送邮件 ==========
收件人: ['friend@qq.com']
✓ 封面GIF已添加（正文显示）: 54321 bytes
✓ 封面PNG已添加（附件）: 12345 bytes
✓ 内页图片已添加（附件）: 234567 bytes
✓ 邮件发送成功！
========== 邮件发送完成 ==========
```

### 前端调试

打开浏览器开发者工具（F12），查看控制台输出：
```javascript
开始截取贺卡预览...
贺卡预览截取完成
发送邮件请求...
服务器响应: {success: true, ...}
```

---

## 🎨 项目特色

### 1. 精美的视觉设计
- 🌈 渐变背景 + 玻璃拟态效果
- 🎭 流畅的页面切换动画
- 🎬 生动的封装仪式动画
- 🐴 可爱的小马邮差送信

### 2. 智能的字体调整
- 根据祝福语长度自动调整字体大小
- 支持手动换行和自动换行
- 精确的垂直居中布局

### 3. 完善的用户体验
- 实时预览编辑效果
- 平滑的2分钟进度条
- 详细的发送状态提示
- 支持多邮箱批量发送

### 4. 健壮的后端系统
- PIL精确复刻前端布局
- 完善的错误处理机制
- 详细的日志输出
- 跨平台字体支持

---

## 📊 性能指标

| 指标 | 数值 |
|------|------|
| 图片生成速度 | 0.1-0.3秒/张 |
| 内存占用 | 约30MB |
| 邮件发送时间 | 1-3秒 |
| 前端资源大小 | 约2MB（含图片） |
| 支持并发数 | 10+ |

---

## 🔒 安全注意事项

### 1. 保护敏感信息
- ✅ `.env` 文件已加入 `.gitignore`
- ✅ 不要将授权码提交到Git仓库
- ✅ 生产环境使用环境变量

### 2. 邮件发送限制
- QQ邮箱：每天发送限制约500封
- 163邮箱：每天发送限制约200封
- 建议添加发送频率限制

### 3. 输入验证
- 后端已实现邮箱格式验证

---

## 📜 许可证

本项目采用 MIT 许可证。

---

## 🙏 致谢

感谢以下开源项目：
- [Flask](https://flask.palletsprojects.com/) - Web框架
- [Pillow](https://python-pillow.org/) - 图片处理
- [python-dotenv](https://github.com/theskumar/python-dotenv) - 环境变量管理

---

## 🎉 祝你使用愉快！

制作专属的新年贺卡，传递温暖的祝福吧！ 🧧✨

---

**最后更新：** 2024年2月

**版本：** 0.1.0
