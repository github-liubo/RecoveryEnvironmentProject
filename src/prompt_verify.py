import tkinter as tk
from tkinter import messagebox
import program_over
from window_icon import get_icon_path
# 全局变量
app_window = None
status_label = None
VERSION = "v1.16"  # 版本号配置（在这里修改版本）

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
