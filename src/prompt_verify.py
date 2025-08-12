import tkinter as tk
from tkinter import messagebox
import program_over
from window_icon import get_icon_path
from image_process_taskbar import load_title_bar_icon
# 全局变量
app_window = None
status_label = None
VERSION = "v1.18"  # 版本号配置

def show_progress_message():
    """显示恢复进度窗口（带自定义美化标题栏）"""
    global app_window, status_label, icon_label  # 保留icon_label全局引用
    icon_path = get_icon_path()  # 假设该函数已定义
    # print(f"拿到的图像地址：{icon_path}")
    drag_data = [0, 0]  # 拖拽坐标存储

    # 创建主窗口
    app_window = tk.Tk()
    app_window.withdraw()
    app_window.overrideredirect(True)
    app_window.resizable(False, False)

    # 窗口尺寸与位置
    window_width = 200
    window_height = 120
    screen_height = app_window.winfo_screenheight()
    x = 0
    y = screen_height - window_height - 80
    app_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # 自定义标题栏
    title_bar = tk.Frame(
        app_window,
        bg="#2c3e50",
        height=30,
        relief=tk.RAISED,
        bd=1
    )
    title_bar.pack(fill=tk.X)

    # 调用外部模块的函数加载图标，并接收返回的icon_label
    icon_label = load_title_bar_icon(title_bar, icon_path)

    # 标题文字
    title_text = tk.Label(
        title_bar,
        text="系 统 恢 复",
        font=("微软雅黑", 10, "bold"),
        bg="#2c3e50",

        fg="#ffffff",
        # padx=5
    )
    title_text.pack(side=tk.LEFT, padx=5)

    # 标题栏拖拽功能
    def on_drag_start(event):
        drag_data[0] = event.x
        drag_data[1] = event.y

    def on_drag_move(event):
        new_x = app_window.winfo_x() + event.x - drag_data[0]
        new_y = app_window.winfo_y() + event.y - drag_data[1]
        app_window.geometry(f"+{new_x}+{new_y}")

    title_bar.bind("<ButtonPress-1>", on_drag_start)
    title_bar.bind("<B1-Motion>", on_drag_move)

    # 标题栏鼠标悬停效果（使用从外部函数获取的icon_label）
    def on_enter(e):
        title_bar.config(bg="#34495e")
        title_text.config(bg="#34495e")
        if icon_label is not None:  # 仅当图标存在时才修改背景
            icon_label.config(bg="#2c3e50")

    def on_leave(e):
        title_bar.config(bg="#2c3e50")
        title_text.config(bg="#2c3e50")
        if icon_label is not None:  # 仅当图标存在时才修改背景
            icon_label.config(bg="#2c3e50")

    title_bar.bind("<Enter>", on_enter)
    title_bar.bind("<Leave>", on_leave)

    # 主内容区域
    content_frame = tk.Frame(app_window)
    content_frame.pack(fill=tk.BOTH, expand=True)

    status_label = tk.Label(
        content_frame,
        text="恢复中，先不要操作",
        font=("微软雅黑", 12),
        wraplength=200,
        justify="center",
        anchor = "center"
    )
    status_label.pack(expand=True, fill=tk.BOTH, pady=(20, 0))

    version_label = tk.Label(
        content_frame,
        text=VERSION,
        font=("微软雅黑", 8),
        fg="#666666"
    )
    version_label.pack(side=tk.RIGHT, anchor=tk.SE, padx=5, pady=5)

    # 链式调用关闭程序
    app_window.after(500, program_over.close_program)

    app_window.deiconify()
    app_window.mainloop()


def show_completion_message():
    """更新提示为“恢复完毕”，5秒后关闭"""
    global status_label, app_window

    if status_label and app_window:
        # 更新文本为青草色
        status_label.config(text="已恢复，5秒后退出", fg="#32CD32")

        # 5秒后关闭窗口并终止程序
        def close_and_quit():
            if app_window.winfo_exists():
                app_window.destroy()
            # 退出主循环
            root = tk._default_root
            if root and root.winfo_exists():
                root.destroy()
            print("恢复任务已完成，程序退出")

        app_window.after(5000, close_and_quit)
        print("恢复任务已完成")
    else:
        print("窗口未初始化，无法更新状态")