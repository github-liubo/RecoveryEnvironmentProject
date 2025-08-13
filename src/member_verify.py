import tkinter as tk
from datetime import datetime, timedelta
from window_icon import get_icon_path
from prompt_verify import show_progress_message
from tkinter import messagebox
from email_verify import generate_verification_code, send_code_to_netease, verify_code_input
import winreg  # 添加Windows注册表操作模块

PASSWORD = "0605xz"  # 默认密码，可修改
INITIAL_VALID_DATE = datetime(2025, 8, 1)  #
REGISTRY_PATH = r"SOFTWARE\RecoveryEnvironment"
REGISTRY_KEY = "ValidUntil"
def load_valid_date():
    """从注册表加载有效期"""
    try:
        # 打开注册表键
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_PATH, 0, winreg.KEY_READ)
        # 读取有效期值
        value, _ = winreg.QueryValueEx(key, REGISTRY_KEY)
        winreg.CloseKey(key)
        # 将字符串转换为datetime对象
        return datetime.strptime(value, "%Y-%m-%d")
    except (WindowsError, FileNotFoundError, ValueError):
        # 如果注册表不存在或值无效，返回初始日期
        return INITIAL_VALID_DATE


def save_valid_date(valid_date):
    """将有效期保存到注册表"""
    try:
        # 创建或打开注册表键
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, REGISTRY_PATH)
        # 将日期转换为字符串并保存
        winreg.SetValueEx(key, REGISTRY_KEY, 0, winreg.REG_SZ, valid_date.strftime("%Y-%m-%d"))
        winreg.CloseKey(key)
    except WindowsError:
        # 如果保存失败，显示错误但不中断程序
        messagebox.showwarning("警告", "无法保存有效期信息，程序将在下次启动时重新验证")


def verify_password():
    """验证用户输入的密码"""
    password = password_entry.get()
    if password == PASSWORD:
        password_window.destroy()  # 关闭密码窗口
        show_progress_message()  # 显示恢复窗口
    else:
        messagebox.showerror("密码错误", "输入的密码不正确，请重试！")
        password_entry.delete(0, tk.END)  # 清空输入框


def show_password_window():
    """显示密码输入窗口"""
    global password_window, password_entry
    icon_path = get_icon_path()
    # 获取全局主窗口（由主函数初始化的 root）
    root = tk._default_root
    if root is None:
        root = tk.Tk()
        root.withdraw()
    password_window = tk.Toplevel(root)
    password_window.withdraw()
    password_window.title("身份验证")
    password_window.geometry("300x150")
    password_window.resizable(False, False)
    # 居中显示
    screen_width = password_window.winfo_screenwidth()
    screen_height = password_window.winfo_screenheight()
    x = (screen_width // 2) - 150
    y = (screen_height // 2) - 75
    password_window.geometry(f"+{x}+{y}")
    password_window.iconbitmap(icon_path)
    password_window.deiconify()  # 显示窗体

    def on_close():
        # 关闭窗口并终止相关流程
        password_window.destroy()
        # 如果主程序依赖root循环，可调用root.quit()确保退出
        if root:
            root.quit()  # 终止主事件循环，避免卡住

    # 绑定关闭按钮事件
    password_window.protocol("WM_DELETE_WINDOW", on_close)
    # 密码提示
    tk.Label(
        password_window,
        text="请输入管理员密码:",
        font=("微软雅黑", 12)
    ).pack(pady=10)

    # 密码输入框
    password_entry = tk.Entry(password_window, show="*", font=("微软雅黑", 12))
    password_entry.pack(pady=10, padx=20, fill=tk.X)
    password_entry.focus_set()  # 自动聚焦到输入框

    # 确认按钮
    tk.Button(
        password_window,
        text="确认",
        command=verify_password,
        font=("微软雅黑", 10),
        width=10,
    ).pack(pady=10)
    # 版本信息标签（右下角）
    tk.Label(
        password_window,
        # text=VERSION,
        font=("微软雅黑", 8),
        fg="gray"  # 灰色文字，不抢眼
    ).place(
        x=285,  # 距离窗口左侧260像素（根据窗口宽度300调整）
        y=120,  # 距离窗口顶部120像素（根据窗口高度150调整）
        anchor="ne"  # 锚点设为右上角，确保文字靠右对齐
    )

    # 绑定回车键到验证函数
    password_window.bind("<Return>", lambda event: verify_password())

    password_window.wait_window(password_window)


def check_date_limit():
    """检查当前日期是否超过有效期，若过期则要求邮箱验证"""
    current_valid_date = load_valid_date()
    current_date = datetime.now()

    if current_date <= current_valid_date:
        return True
    else:
        messagebox.showinfo("使用限制", "使用期限已过，请通过邮箱验证码延长")

        code = generate_verification_code()
        print(f"输入的验证码为{code}")
        if not send_code_to_netease(code):
            messagebox.showerror("错误", "发送验证码失败，请检查邮箱配置")
            return False

        EXTEND_DAYS = 30
        if verify_code_input(code):
            # 计算理论延长后的日期
            理论延长日期 = current_date + timedelta(days=EXTEND_DAYS)
            # 关键修复：限制延长后的日期不得超过最终授权期限
            new_valid_date = min(理论延长日期, EXPIRY_DATE)  # 取较小值

            save_valid_date(new_valid_date)
            # 提示信息中明确实际延长到的日期（可能是理论值或最终期限）
            messagebox.showinfo(
                "成功",
                f"验证通过，有效期延长至：{new_valid_date.strftime('%Y-%m-%d')}"
            )
            return True
        else:
            messagebox.showerror("失败", "验证码错误，无法继续使用")
            return False

EXPIRY_DATE = datetime(2025, 8, 31)
def time_verification():
    """主验证流程：检查日期 -> 邮箱验证 -> 密码验证"""
    # 获取主窗口（通过Tkinter默认根窗口，与主函数的root关联）
    root = tk._default_root  # 关联主函数初始化的root

    # 检查当前日期是否超过最终截止日
    current_date = datetime.now()
    if current_date > EXPIRY_DATE:
        messagebox.showerror("授权过期", "软件授权过期，请联系管理员更新授权！")

        # 关键修复：授权过期时，主动终止主循环并销毁窗口
        if root:
            # root.quit()  # 终止主事件循环
            root.destroy()  # 销毁主窗口，释放资源
        return False  # 验证失败

    # 检查使用期限
    if not check_date_limit():
        # 日期验证失败时，同样终止程序（可选，根据需求调整）
        if root:
            # root.quit()
            root.destroy()
        return False  # 验证失败

    # 所有验证通过，返回True
    return True