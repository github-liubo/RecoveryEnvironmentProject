import tkinter as tk
# from threading import Thread
# import time
from tkinter import messagebox
from datetime import datetime
import program_over
from window_icon import get_icon_path
# 全局变量
app_window = None
status_label = None
PASSWORD = "0605xz"  # 默认密码，可修改
EXPIRY_DATE = datetime(2025, 8, 31)  # 密码有效期截止日
VERSION = "v1.15"  # 版本号配置（在这里修改版本）

def verify_password():
    # 获取当前日期
    current_date = datetime.now()

    # 检查密码有效期
    if current_date > EXPIRY_DATE:
        messagebox.showerror("密码过期", "管理员密码已过期，请联系系统管理员！")
        password_entry.delete(0, tk.END)  # 清空输入框
        return
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
        text=VERSION,
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


def show_progress_message():
    """显示恢复进度窗口"""
    global app_window, status_label
    icon_path = get_icon_path()
    # 创建主窗口
    app_window = tk.Tk()
    app_window.withdraw() # 隐藏窗体
    app_window.title("系统提示")
    app_window.resizable(False, False)
    # 设置窗口大小并定位到左下角
    window_width = 400
    window_height = 110
    screen_height = app_window.winfo_screenheight()
    x = 0  # 距屏幕左侧0像素
    y = screen_height - window_height - 80  # 距屏幕底部100像素
    app_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    app_window.iconbitmap(icon_path)
    app_window.deiconify()  # 显示窗体
    # 创建标签（文本完全居中）
    status_label = tk.Label(
        app_window,
        text="正在恢复，请先不要操作",
        font=("微软雅黑", 14),
        wraplength=350,
        justify="center"
    )
    status_label.pack(expand=True)  # 文本在窗口中完全居中
    #链式调用 关闭多个程序
    app_window.after(500, program_over.close_program)
    # 启动 GUI 主循环
    app_window.mainloop()


# 函数2：更新提示为“恢复完毕”，5秒后关闭
def show_completion_message():
    global status_label, app_window

    if status_label and app_window:
        # 更新文本,青草色
        status_label.config(text="恢复完毕，5秒后关闭窗口",fg="#32CD32")
        # 5秒后关闭恢复窗口，并彻底终止程序
        def close_and_quit():
            # global root  # 显式引用全局root
            # 先关闭恢复窗口
            if app_window.winfo_exists():  # 检查窗口是否存在
                app_window.destroy()
                # 获取 root 并退出主循环
            root = tk._default_root
            if root and root.winfo_exists():
                # root.quit()  # 终止 mainloop
                root.destroy()
            print("恢复任务已完成，程序退出")
        app_window.after(5000, close_and_quit)
        print("恢复任务已完成")
    else:
        print("窗口未初始化，无法更新状态")
