import json
import os
import tkinter as tk
from tkinter import messagebox
import smtplib
import random
from email.mime.text import MIMEText
from email.header import Header

# ======================
# 配置参数（需替换为实际信息）
# ======================
# 启动次数配置
MAX_LAUNCH_COUNT = 12  # 最大启动次数
COUNT_FILE = "C:\\Program Files (x86)\\launch_count.json"  # 注意转义反斜杠

# 验证码邮件配置（发送到网易邮箱）
SMTP_SENDER = "你的发送邮箱@qq.com"  # 发送验证码的邮箱（如QQ邮箱）
SMTP_AUTH_CODE = "你的发送邮箱授权码"  # 发送邮箱的SMTP授权码
SMTP_SERVER = "smtp.qq.com"  # 发送邮箱的SMTP服务器（QQ邮箱为smtp.qq.com）
SMTP_PORT = 465  # SSL端口
RECEIVER_EMAIL = "目标网易邮箱@163.com"  # 接收验证码的网易邮箱


# ======================
# 验证码相关函数
# ======================
def generate_verification_code():
    """生成6位随机验证码"""
    return "".join([str(random.randint(0, 9)) for _ in range(6)])


def send_code_to_netease(receiver, code):
    """发送验证码到网易邮箱"""
    try:
        # 构造邮件内容
        msg = MIMEText(
            f"你的使用次数已达上限，验证码：{code}\n输入验证码可重置次数，有效期5分钟。",
            "plain",
            "utf-8"
        )
        msg["Subject"] = Header("【使用次数重置验证码】", "utf-8")
        msg["From"] = Header(f"系统通知 <{SMTP_SENDER}>", "utf-8")
        msg["To"] = Header(receiver, "utf-8")

        # 发送邮件
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_SENDER, SMTP_AUTH_CODE)
            server.sendmail(SMTP_SENDER, receiver, msg.as_string())
        return True
    except Exception as e:
        print(f"邮件发送失败：{e}")
        return False


def verify_code_input(real_code):
    """显示验证码输入窗口，返回验证结果"""
    verify_window = tk.Toplevel()
    verify_window.title("验证重置次数")
    verify_window.geometry("300x180")
    verify_window.resizable(False, False)
    verify_window.transient()  # 设为主窗口的子窗口
    verify_window.grab_set()  # 模态窗口（阻止其他窗口操作）

    # 居中显示
    screen_width = verify_window.winfo_screenwidth()
    screen_height = verify_window.winfo_screenheight()
    x = (screen_width // 2) - 150
    y = (screen_height // 2) - 90
    verify_window.geometry(f"+{x}+{y}")

    # 提示文本
    tk.Label(
        verify_window,
        text="使用次数已达上限，请输入邮箱收到的验证码",
        font=("微软雅黑", 10),
        wraplength=280
    ).pack(pady=15)

    # 输入框
    code_var = tk.StringVar()
    tk.Entry(
        verify_window,
        textvariable=code_var,
        font=("微软雅黑", 12),
        width=10,
        justify="center"
    ).pack(pady=10)

    # 验证结果变量
    result = [False]  # 用列表存储（可变对象）

    def check_input():
        """检查输入的验证码是否正确"""
        user_input = code_var.get().strip()
        if user_input == real_code:
            result[0] = True
            verify_window.destroy()
        else:
            messagebox.showerror("错误", "验证码不正确，请重新输入")

    # 确认按钮
    tk.Button(
        verify_window,
        text="确认",
        command=check_input,
        font=("微软雅黑", 10),
        width=10
    ).pack(pady=10)

    verify_window.mainloop()
    return result[0]


# ======================
# 启动次数相关函数
# ======================
def load_launch_count():
    """读取启动次数"""
    if os.path.exists(COUNT_FILE):
        try:
            with open(COUNT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("count", 0)
        except (json.JSONDecodeError, IOError) as e:
            print(f"读取次数失败：{e}")
            return 0  # 文件损坏时重置
    else:
        save_launch_count(0)  # 首次启动创建文件
        return 0


def save_launch_count(count):
    """保存启动次数"""
    # 处理Program Files目录的权限问题
    try:
        with open(COUNT_FILE, "w", encoding="utf-8") as f:
            json.dump({"count": count}, f, indent=2)
    except IOError as e:
        messagebox.showerror("错误", f"无法保存次数（权限不足）：{e}")


def check_launch_limit():
    """检查启动次数，超限则触发验证码流程"""
    current_count = load_launch_count()

    # 如果未达上限，直接计数+1
    if current_count < MAX_LAUNCH_COUNT:
        save_launch_count(current_count + 1)
        return True

    # 达到上限，触发验证码流程
    else:
        # 生成并发送验证码
        code = generate_verification_code()
        print(f"调试：生成的验证码为{code}")  # 实际场景可删除

        if not send_code_to_netease(RECEIVER_EMAIL, code):
            messagebox.showerror("错误", "发送验证码失败，请检查邮箱配置")
            return False

        # 验证用户输入
        if verify_code_input(code):
            # 验证通过，重置次数为1（本次启动）
            save_launch_count(1)
            messagebox.showinfo("成功", "验证码正确，次数已重置")
            return True
        else:
            # 验证失败，保持次数不变
            messagebox.showerror("失败", "验证码错误，无法继续使用")
            return False


# ======================
# 测试入口（实际使用时集成到主程序）
# ======================
if __name__ == "__main__":
    # 模拟程序启动检查
    if check_launch_limit():
        print("程序正常启动")
        # 这里放主程序逻辑
    else:
        print("启动被限制")