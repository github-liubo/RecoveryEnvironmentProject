import tkinter as tk
from tkinter import messagebox
import program_over
from window_icon import get_icon_path

# 全局变量
app_window = None
status_label = None
VERSION = "v1.16"  # 版本号配置


def show_progress_message():
    """显示恢复进度窗口（带自定义美化标题栏）"""
    global app_window, status_label
    icon_path = get_icon_path()

    # 存储拖拽相关数据（用于标题栏拖拽）
    drag_data = [0, 0]  # [x, y]

    # 创建主窗口
    app_window = tk.Tk()
    app_window.withdraw()  # 先隐藏窗体
    app_window.overrideredirect(True)  # 隐藏系统标题栏（关键：移除默认关闭按钮等）
    app_window.resizable(False, False)

    # 窗口尺寸与位置（左下角定位）
    window_width = 200
    window_height = 120
    screen_height = app_window.winfo_screenheight()
    x = 0  # 距屏幕左侧0像素
    y = screen_height - window_height - 80  # 距屏幕底部100像素
    app_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # --------------------------
    # 自定义美化标题栏
    # --------------------------
    # 标题栏样式：深蓝色背景，轻微凸起效果
    title_bar = tk.Frame(
        app_window,
        bg="#2c3e50",  # 深蓝主色
        height=30,
        relief=tk.RAISED,
        bd=1
    )
    title_bar.pack(fill=tk.X)  # 横向填充窗口

    # 左上角图标（保留原图标逻辑）
    if icon_path:
        try:
            # 加载并缩放图标以适应标题栏（30x30）
            icon_img = tk.PhotoImage(file=icon_path)
            # 计算缩放比例（确保图标不超过30x30）
            scale_w = max(1, icon_img.width() // 30)
            scale_h = max(1, icon_img.height() // 30)
            icon_img = icon_img.subsample(scale_w, scale_h)

            # 放置图标
            icon_label = tk.Label(
                title_bar,
                image=icon_img,
                bg="#2c3e50",  # 与标题栏背景一致
                padx=5  # 右侧留白
            )
            icon_label.image = icon_img  # 保留引用，防止被垃圾回收
            icon_label.pack(side=tk.LEFT, fill=tk.Y)
        except Exception as e:
            print(f"图标加载失败: {e}")
            # 图标加载失败时，用空白占位
            tk.Label(title_bar, width=4, bg="#2c3e50").pack(side=tk.LEFT, fill=tk.Y)
    else:
        # 无图标路径时，空白占位
        tk.Label(title_bar, width=4, bg="#2c3e50").pack(side=tk.LEFT, fill=tk.Y)

    # 标题文字（居中显示在标题栏）
    title_text = tk.Label(
        title_bar,
        text="系统恢复",  # 更明确的标题
        font=("微软雅黑", 10, "bold"),  # 加粗字体
        bg="#2c3e50",
        fg="#ffffff",  # 白色文字，与深色背景对比
        padx=5
    )
    title_text.pack(side=tk.LEFT, fill=tk.Y, expand=True)  # 横向扩展居中

    # 标题栏拖拽功能（窗口可拖动）
    def on_drag_start(event):
        # 记录鼠标按下时的坐标
        drag_data[0] = event.x
        drag_data[1] = event.y

    def on_drag_move(event):
        # 计算新位置并移动窗口
        new_x = app_window.winfo_x() + event.x - drag_data[0]
        new_y = app_window.winfo_y() + event.y - drag_data[1]
        app_window.geometry(f"+{new_x}+{new_y}")

    # 绑定拖拽事件（点击标题栏任意位置均可拖动）
    title_bar.bind("<ButtonPress-1>", on_drag_start)
    title_bar.bind("<B1-Motion>", on_drag_move)

    # 标题栏鼠标悬停效果（增强交互感）
    def on_enter(e):
        title_bar.config(bg="#34495e")  # 稍浅的蓝色
        title_text.config(bg="#34495e")
        if icon_path:
            try:
                icon_label.config(bg="#34495e")
            except:
                pass

    def on_leave(e):
        title_bar.config(bg="#2c3e50")  # 恢复原颜色
        title_text.config(bg="#2c3e50")
        if icon_path:
            try:
                icon_label.config(bg="#2c3e50")
            except:
                pass

    title_bar.bind("<Enter>", on_enter)
    title_bar.bind("<Leave>", on_leave)

    # --------------------------
    # 主内容区域（含状态提示和版本号）
    # --------------------------
    content_frame = tk.Frame(app_window)
    content_frame.pack(fill=tk.BOTH, expand=True)

    # 状态提示标签（居中）
    status_label = tk.Label(
        content_frame,
        text="恢复中，先不要操作",
        font=("微软雅黑", 12),
        wraplength=200,
        justify="center"
    )
    status_label.pack(expand=True)  # 垂直居中

    # 右下角版本号
    version_label = tk.Label(
        content_frame,
        text=VERSION,
        font=("微软雅黑", 8),  # 小一号字体
        fg="#666666"  # 灰色，不抢眼
    )
    version_label.pack(side=tk.RIGHT, anchor=tk.SE, padx=5, pady=5)  # 右下角定位

    # 链式调用：关闭程序
    app_window.after(500, program_over.close_program)

    # 显示窗体并启动主循环
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