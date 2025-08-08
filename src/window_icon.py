import sys, os
def get_icon_path():
    # 统一使用 os.path.join 处理路径，自动适配系统分隔符
    if getattr(sys, 'frozen', False):
        # 打包后环境
        return os.path.join(sys._MEIPASS, "assets", "images", "recover.jpg")
    else:
        # 开发环境
        return os.path.abspath(os.path.join(
            os.path.dirname(__file__),  # 当前文件所在目录
            "..", "assets", "images", "recover.jpg"
        ))
