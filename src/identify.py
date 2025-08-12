import pyautogui
import time
import pygetwindow as gw  # 用于检查窗口是否存在
import win32gui
import sys
import os

def enum_window(hwnd, windows):
    if win32gui.IsWindowVisible(hwnd):
        window_title = win32gui.GetWindowText(hwnd)
        if window_title:  # 忽略没有标题的窗口
            rect = win32gui.GetWindowRect(hwnd)
            windows.append({
                'hwnd': hwnd,
                'title': window_title,
                'left': rect[0],
                'top': rect[1],
                'width': rect[2] - rect[0],
                'height': rect[3] - rect[1]
            })


def get_window_rect_by_title(title):
    """
    使用 win32gui 获取特定标题的窗口位置和大小。
    :param title: 目标窗口的标题（部分匹配）
    :return: 窗口信息字典或 None
    """
    windows = []
    win32gui.EnumWindows(enum_window, windows)
    for w in windows:
        if title in w['title']:
            return w
    return None


def click_image_in_window(window, image_path, confidence=0.8, timeout=10):
    """
    在指定窗口中持续查找图片，直到找到并点击，或超时。

    :param window: 目标窗口对象（pyautogui 的 Window 实例）
    :param image_path: 要查找的图片路径（.png 格式）
    :param confidence: 匹配精度（0~1）
    :param timeout: 超时时间（秒）
    :return: bool - 是否成功点击
    """
    print(f"正在查找图片: {image_path} (匹配精度: {confidence})")
    # print(f"目标窗口标题: {window.title}")  # 打印传入的窗口标题
    # all_titles = gw.getAllTitles()
    # print(f"所有窗口标题: {all_titles}")  # 打印系统中所有窗口标题
    # if window.title not in all_titles:
    #     print("目标窗口未匹配到！")

    end_time = time.time() + timeout

    while time.time() < end_time:
        try:
            time.sleep(0.5)  # 控制查找频率

            # 使用 win32gui 获取窗口信息作为备选方案
            alt_window_info = get_window_rect_by_title(window.title)
            if alt_window_info:
                x, y, width, height = alt_window_info['left'], alt_window_info['top'], alt_window_info['width'], \
                alt_window_info['height']
            else:
                # 如果 win32gui 未能找到，则尝试使用 pygetwindow
                if window.title not in gw.getAllTitles():
                    print("目标窗口已关闭或不存在")
                    return False
                x, y = window.left, window.top
                width, height = window.width, window.height

            # 检查窗口是否最小化（宽高为0）
            if width <= 0 or height <= 0:
                print("窗口可能已最小化或隐藏")
                time.sleep(0.5)
                continue

            region = (x, y, width, height)

            # 查找图像
            location = pyautogui.locateOnScreen(
                image_path,
                region=region,
                confidence=confidence,
                grayscale=True
            )

            if location:
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                print(f"✅ 找到图片 {image_path}，已在位置 ({center_x}, {center_y}) 点击")
                # 关键：点击后将鼠标移开目标图片区域（比如移到窗口右上角）
                pyautogui.moveTo(x + width - 10, y + 10)  # 移到窗口右上角（远离图片）
                return True

        except pyautogui.ImageNotFoundException:
            # 图像未找到，继续循环
            pass
        except Exception as e:
            # 打印异常但不停止循环
            print(f"❌ 查找图片时发生异常: {e}")
            time.sleep(0.5)

    print(f"❌ 超时({timeout}s)：在窗口中未找到图片 {image_path}")
    return False


def resource_path(relative_path):
    """ 获取资源的绝对路径，兼容开发环境和打包环境 """
    try:
        # PyInstaller 创建临时文件夹，路径存储在 _MEIPASS 中
        base_path = sys._MEIPASS
    except Exception:
        current_script_dir = os.path.abspath(os.path.dirname(__file__))  # src目录
        base_path = os.path.dirname(current_script_dir)  # 项目根目录（src的上一级）

    return os.path.join(base_path, relative_path)