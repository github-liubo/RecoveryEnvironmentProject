from PIL import Image, ImageTk
import tkinter as tk
import traceback


def load_title_bar_icon(title_bar, icon_path):
    """加载标题栏图标并返回标签实例，明确绑定到当前窗口"""
    try:
        if icon_path:
            # 用PIL加载图像
            img = Image.open(icon_path)
            img.thumbnail((18, 18))  # 缩放

            # 关键修改：通过master参数绑定到title_bar（关联当前窗口）
            icon_img = ImageTk.PhotoImage(img, master=title_bar)

            # 创建图标标签，父组件是title_bar（确保与窗口关联）
            icon_label = tk.Label(
                title_bar,
                image=icon_img,
                bg="#2c3e50",
                padx=5
            )
            icon_label.image = icon_img  # 强制保留引用，防止回收
            icon_label.pack(side=tk.LEFT, fill=tk.Y)
            print(f"成功加载图标: {icon_path}")
            return icon_label

        # 无图标路径时返回空白标签
        else:
            print("无图标路径，使用空白占位")
            return None

    except Exception as e:
        print(f"图标加载失败: {e}")
        traceback.print_exc()
        return None