# 🚀 快速配置指南

## 第一步：安装依赖

打开终端，进入项目目录，运行：

```bash
pip install -r requirements.txt
```

等待安装完成，看到类似输出：
```
Successfully installed Flask-3.0.0 Flask-Cors-4.0.0 Pillow-10.1.0 ...
```

---

## 第二步：配置邮箱

### 方式一：编辑.env文件（推荐）

1. 打开项目目录中的 `.env` 文件

2. 将以下内容替换为你的邮箱信息：

```env
SMTP_USERNAME=your_email@qq.com
SMTP_PASSWORD=your_authorization_code
SMTP_HOST=smtp.qq.com
SMTP_PORT=587
```

### 方式二：参考示例配置

如果不确定如何填写，可以查看 `.env.example` 文件中的详细说明和示例。

---

## 第三步：获取QQ邮箱授权码

### 详细步骤：

1. **登录QQ邮箱**
   - 访问：https://mail.qq.com
   - 使用QQ账号登录

2. **进入设置**
   - 点击页面顶部的 **设置** 按钮
   - 选择 **账户** 选项卡

3. **开启SMTP服务**
   - 向下滚动，找到 **POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务**
   - 找到 **POP3/SMTP服务** 或 **IMAP/SMTP服务**
   - 点击右侧的 **开启** 按钮

4. **生成授权码**
   - 点击 **生成授权码** 按钮
   - 根据提示发送短信到指定号码
   - 稍等片刻，页面会显示一个16位的授权码
   - 例如：`abcdefghijklmnop`

5. **复制授权码**
   - 选中授权码
   - 按 Ctrl+C 复制（或右键复制）
   - ⚠️ 注意：这是授权码，不是你的QQ密码！

6. **填入.env文件**
   ```env
   SMTP_USERNAME=1234567890@qq.com
   SMTP_PASSWORD=abcdefghijklmnop
   ```

---

## 第四步：启动服务器

### 方式一：命令行启动

在项目目录下运行：
```bash
python server.py
```

看到以下输出表示成功：
```
============================================================
新年电子贺卡 - 后端服务器 (PIL图片生成版)
============================================================
服务地址: http://localhost:5000

============================================================
启动开发服务器...
============================================================
 * Running on http://0.0.0.0:5000
```

### 方式二：VS Code中启动

1. 在VS Code中打开 `server.py`
2. 按 `F5` 键（或点击右上角的运行按钮）
3. 选择 "Python File"
4. 看到相同的输出信息

---

## 第五步：访问应用

打开浏览器，输入：
```
http://localhost:5000
```

现在你应该能看到新年贺卡制作页面了！🎉

---

## 常见问题速查

### ❌ 问题1：pip install 失败

**解决：** 尝试使用国内镜像
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### ❌ 问题2：提示"SMTP配置不完整"

**检查：**
1. `.env` 文件是否在项目根目录
2. `SMTP_USERNAME` 和 `SMTP_PASSWORD` 是否已填写
3. 确保没有多余的空格或引号

**正确格式：**
```env
SMTP_USERNAME=1234567890@qq.com
SMTP_PASSWORD=abcdefghijklmnop
```

**错误格式：**
```env
SMTP_USERNAME="1234567890@qq.com"  ❌ 不要加引号
SMTP_PASSWORD = abcdefghijklmnop   ❌ 等号两边不要有空格
```

### ❌ 问题3：发送邮件失败

**原因：** 可能是使用了登录密码而不是授权码

**解决：**
1. 确认你填写的是授权码（16位字母）
2. 不是QQ密码（数字+字母的登录密码）
3. 重新生成授权码并替换

### ❌ 问题4：VS Code无法运行

**解决：**
1. 安装Python扩展
   - 按 Ctrl+Shift+X 打开扩展
   - 搜索 "Python"
   - 安装Microsoft官方的Python扩展

2. 选择Python解释器
   - 按 Ctrl+Shift+P
   - 输入 "Python: Select Interpreter"
   - 选择你安装的Python版本

---

## 验证配置是否成功

### 1. 检查依赖安装

运行以下命令：
```bash
python -c "import flask, PIL; print('依赖安装成功！')"
```

如果看到 `依赖安装成功！` 表示OK。

### 2. 检查.env配置

运行以下命令：
```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('SMTP用户:', os.getenv('SMTP_USERNAME'))"
```

应该显示你配置的邮箱地址。

### 3. 测试发送

1. 启动服务器
2. 访问 http://localhost:5000
3. 制作一张贺卡
4. 输入自己的邮箱测试
5. 查看邮箱是否收到

---

## 🎉 配置完成！

现在你可以：
- ✅ 制作精美的新年贺卡
- ✅ 发送给任意邮箱
- ✅ 享受完整的动画效果

祝你使用愉快！🧧✨
