import smtplib
import poplib
import re
import time
import ssl
import random
from email.mime.text import MIMEText
from email.header import Header, decode_header
from email.parser import BytesParser
from bs4 import BeautifulSoup
import tkinter as tk
from window_icon import get_icon_path
# ======================
# 配置参数（需替换为实际信息）
# ======================
# 发送方邮箱（如QQ邮箱，需开启SMTP）
SMTP_SENDER = "liuworkbo@163.com"  # 示例：xxx@qq.com
SMTP_AUTH_CODE = "ACcK5GCnfsFnDHFG"  # QQ邮箱SMTP授权码
SMTP_SERVER = "smtp.163.com"  # QQ邮箱SMTP服务器
SMTP_PORT = 465  # SSL端口

# 接收方网易邮箱（目标邮箱）
RECEIVER_EMAIL = "liuworkbo@163.com"  # 示例：liuworkbo@163.com
POP_AUTH_CODE = "ACcK5GCnfsFnDHFG"  # 网易邮箱POP3授权码


# ======================
# 1. 生成6位随机验证码
# ======================
def generate_verification_code():
    """生成6位随机数字验证码"""
    return "".join([str(random.randint(0, 9)) for _ in range(6)])


# ======================
# 2. 发送验证码到网易邮箱
# ======================
def send_code_to_netease(code):
    receiver=RECEIVER_EMAIL
    """通过SMTP发送验证码邮件到网易邮箱"""
    # 构造邮件内容
    msg = MIMEText(
        f"你的验证码是：{code}\n有效期5分钟，请及时填写。",
        "plain",
        "utf-8"
    )
    msg["Subject"] = Header("【验证码】请确认你的操作", "utf-8")
    msg["From"] = Header(f"验证系统 <{SMTP_SENDER}>", "utf-8")
    msg["To"] = Header(receiver, "utf-8")

    try:
        # 连接SMTP服务器并发送
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_SENDER, SMTP_AUTH_CODE)
            server.sendmail(SMTP_SENDER, receiver, msg.as_string())
            # print(f"✅ 验证码已发送到 {receiver}")
            print(f"✅ 验证码已发送到")
        return True
    except Exception as e:
        print(f"❌ 发送失败：{str(e)}")
        return False


# ======================
# 3. 从网易邮箱读取验证码（优化版）
# ======================
def decode_mime_words(s):
    """解码邮件头中文"""
    if not s:
        return ""
    decoded_fragments = decode_header(s)
    fragments = []
    for content, charset in decoded_fragments:
        if isinstance(content, bytes):
            if charset:
                try:
                    fragments.append(content.decode(charset))
                except:
                    fragments.append(content.decode('utf-8', errors='ignore'))
            else:
                fragments.append(content.decode('utf-8', errors='ignore'))
        else:
            fragments.append(content)
    return ''.join(fragments)

def clean_html_text(html_content):
    """清理HTML标签"""
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text(separator=" ").strip()
    return re.sub(r'\s+', ' ', text)

def read_code_from_netease(email, auth_code, timeout=60):
    """从网易邮箱读取最新验证码"""
    pop_server = None
    parser = BytesParser()
    context = ssl.create_default_context()

    try:
        # 连接网易POP3服务器
        pop_server = poplib.POP3_SSL('pop.163.com', 995, context=context)
        pop_server.user(email)
        pop_server.pass_(auth_code)
        print("✅ 已连接邮箱，开始读取验证码...")

        start_time = time.time()
        while time.time() - start_time < timeout:
            # 获取邮件数量
            num_messages = len(pop_server.list()[1])
            if num_messages == 0:
                time.sleep(3)
                continue

            # 从最新邮件开始查找
            for mail_index in range(num_messages, 0, -1):
                try:
                    # 读取邮件内容
                    raw_email = b'\r\n'.join(pop_server.retr(mail_index)[1])
                    msg = parser.parsebytes(raw_email)

                    # 解析发件人和主题（过滤无关邮件）
                    from_addr = decode_mime_words(msg.get("From", ""))
                    subject = decode_mime_words(msg["Subject"])
                    if "验证码" not in subject and SMTP_SENDER not in from_addr:
                        continue  # 跳过非验证码邮件

                    # 提取并清理正文
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() in ["text/plain", "text/html"]:
                                payload = part.get_payload(decode=True)
                                if payload:
                                    for encoding in ['utf-8', 'gbk', 'gb2312']:
                                        try:
                                            body = payload.decode(encoding)
                                            break
                                        except:
                                            continue
                                if body:
                                    break
                    else:
                        payload = msg.get_payload(decode=True)
                        if payload:
                            body = payload.decode('utf-8', errors='ignore')

                    # 清理HTML并提取验证码
                    cleaned_body = clean_html_text(body)
                    match = re.search(r'验证码是：(\d{6})', cleaned_body)
                    if match:
                        code = match.group(1)
                        print(f"✅ 从邮件中读取到验证码")
                        return code

                except Exception as e:
                    print(f"⚠️ 解析邮件 {mail_index} 失败：{str(e)}")
                    continue

            time.sleep(3)  # 每轮检查间隔

        print(f"❌ 超时{timeout}秒，未读取到验证码")
        return None

    except Exception as e:
        print(f"❌ 读取失败：{str(e)}")
        return None
    finally:
        if pop_server:
            try:
                pop_server.quit()
            except:
                pass


def verify_code_input(code):
    """显示验证码输入窗口（修复版：输入框位置调整）"""
    # 检查主窗口
    root = tk._default_root
    if root is None:
        root = tk.Tk()
        root.withdraw()
    else:
        root.withdraw()  # 隐藏窗体
    icon_path = get_icon_path()

    # 创建对话框（初始隐藏）
    verify_window = tk.Toplevel(root)
    verify_window.withdraw()  # 先隐藏窗口
    verify_window.title("登入身份续期")
    verify_window.geometry("300x150")
    verify_window.resizable(False, False)
    verify_window.configure(bg="#f0f0f0")
    # verify_window.attributes("-topmost", True)

    # 计算居中位置
    verify_window.update_idletasks()  # 更新窗口信息但不显示
    x = (verify_window.winfo_screenwidth() // 2) - (300 // 2)
    y = (verify_window.winfo_screenheight() // 2) - (150 // 2)
    verify_window.geometry(f"+{x}+{y}")

    verify_window.iconbitmap(icon_path)

    # 现在显示窗口（位置已设置好）
    verify_window.deiconify()  # 显示窗体

    # 提示标签
    label = tk.Label(
        verify_window,
        text="请输入邮箱收到的验证码：",
        bg="#f0f0f0",
        font=("微软雅黑", 12)
    )
    label.pack(pady=(20, 20))

    # 外层容器：用于整体调整位置
    outer_frame = tk.Frame(verify_window, bg="#f0f0f0")
    outer_frame.pack(pady=5, padx=(0, 10))  # 左侧留0px边距，整体左移

    # 输入框与按钮容器
    input_frame = tk.Frame(outer_frame, bg="#f0f0f0")
    input_frame.pack()

    # ======================
    # 输入框调整：字体增高+通过外层Frame左移
    # ======================
    code_entry = tk.Entry(
        input_frame,
        font=("微软雅黑", 14),  # 增大字体高度
        width=8,
        justify="center",
        # show="*",
        bd=2  # 边框稍粗
    )
    # 用正值padx调整间距（取消负边距）
    code_entry.pack(side=tk.LEFT, padx=(0, 20))
    # code_entry.focus()

    # 新增：限制输入为6位数字
    def validate_input(text):
        # 允许空字符串（用于清空输入框）
        if not text:
            return True
        if len(text) > 6:
            return False
        return text.isdigit()
    validate_cmd = verify_window.register(validate_input)
    code_entry.config(validate="key", validatecommand=(validate_cmd, "%P"))
    # ======================
    # 确认按钮调整：缩小尺寸
    # ======================
    result = [False]

    def on_confirm():
        user_input = code_entry.get().strip()
        if not user_input:
            error_label.config(text="请输入验证码", fg="red")
            return
        if user_input == code:
            result[0] = True
            verify_window.destroy()
        else:
            error_label.config(text="验证码错误，请重新输入", fg="red")
            code_entry.delete(0, tk.END)

    confirm_btn = tk.Button(
        input_frame,
        text="确认",
        command=on_confirm,
        width=8,
        height=1,
        bg="#4CAF50",
        fg="white",
        font=("微软雅黑", 9),
        padx=5
    )
    confirm_btn.pack(side=tk.LEFT)

    # 错误提示标签
    error_label = tk.Label(
        verify_window,
        text="",
        bg="#f0f0f0",
        fg="red",
        font=("微软雅黑", 9)
    )
    error_label.pack(pady=5,padx=(0, 10))

    # 按钮悬停效果
    def on_enter(e):
        confirm_btn.config(bg="#45a049")

    def on_leave(e):
        confirm_btn.config(bg="#4CAF50")

    confirm_btn.bind("<Enter>", on_enter)
    confirm_btn.bind("<Leave>", on_leave)

    # 回车确认
    verify_window.bind("<Return>", lambda e: on_confirm())

    # 关闭窗口逻辑：确保程序终止
    def on_close():
        result[0] = False
        verify_window.destroy()
        root.quit()  # 关闭窗口时终止主循环

    verify_window.protocol("WM_DELETE_WINDOW", on_close)

    verify_window.lift()
    verify_window.wait_window(verify_window)

    return result[0]
