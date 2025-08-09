import json
import os
import tkinter as tk
from email_verify import generate_verification_code,send_code_to_netease,verify_code_input
from tkinter import messagebox
from window_icon import get_icon_path

# 全局变量：最大启动次数和存储文件路径
MAX_LAUNCH_COUNT = 12  # 最大启动次数
COUNT_FILE = "C:\Program Files (x86)\launch_count.json"  # 存储启动次数的文件

def load_launch_count():
    """读取启动次数（从文件加载）"""
    if os.path.exists(COUNT_FILE):
        try:
            with open(COUNT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("count", 0)
        except (json.JSONDecodeError, IOError):
            return 0  # 文件损坏时重置为0
    else:
        save_launch_count(0)  # 首次启动创建文件
        return 0

def save_launch_count(count):
    """保存启动次数到文件"""
    try:
        with open(COUNT_FILE, "w", encoding="utf-8") as f:
            json.dump({"count": count}, f, indent=2)
    except IOError as e:
        print(f"保存启动次数失败：{e}")


def check_launch_limit():
    current_count = load_launch_count()

    if current_count < MAX_LAUNCH_COUNT:
        save_launch_count(current_count + 1)
        return True
    else:
        show_limit_window()
        code = generate_verification_code()
        print(f"调试：生成的验证码为{code}")

        # 修复：补充接收者邮箱参数
        if not send_code_to_netease(code):
            messagebox.showerror("错误", "发送验证码失败，请检查邮箱配置")
            return False

        # 验证输入（此时 verify_code_input 会正确返回结果）
        if verify_code_input(code):
            save_launch_count(1)  # 重置次数
            messagebox.showinfo("成功", "验证码正确，次数已重置")  # 会正常弹出
            return True
        else:
            messagebox.showerror("失败", "验证码错误，无法继续使用")
            return False

def show_limit_window():
    """显示使用次数超限窗口（修复为子窗口）"""
    icon_path = get_icon_path()
    # 获取全局主窗口（由主函数初始化的 root）
    root = tk._default_root
    if root is None:
        root = tk.Tk()
        root.withdraw()
    limit_window = tk.Toplevel(root)
    limit_window.withdraw()
    limit_window.title("使用限制")
    limit_window.geometry("300x150")
    limit_window.resizable(False, False)

    # 居中显示窗口
    screen_width = limit_window.winfo_screenwidth()
    screen_height = limit_window.winfo_screenheight()
    x = (screen_width // 2) - 175
    y = (screen_height // 2) - 75
    limit_window.geometry(f"+{x}+{y}")
    limit_window.iconbitmap(icon_path)
    limit_window.deiconify()  # 显示窗体
    # 超限提示文本
    tk.Label(
        limit_window,
        text="使用次数超限，请输入管理员验证码",
        font=("微软雅黑", 12, "bold"),
        fg="red"
    ).pack(pady=20)

    # 确认按钮
    tk.Button(
        limit_window,
        text="确定",
        command=limit_window.destroy,
        font=("微软雅黑", 10),
        width=10
    ).pack(pady=10)

    # 替换 mainloop() 为 wait_window()，避免嵌套事件循环
    limit_window.wait_window(limit_window)
