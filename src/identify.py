import pyautogui
import time
import pygetwindow as gw  # 用于检查窗口是否存在

def click_image_in_window(window, image_path, confidence=0.9, timeout=10):
    """
    在指定窗口中持续查找图片，直到找到并点击，或超时。

    :param window: 目标窗口对象（pyautogui 的 Window 实例）
    :param image_path: 要查找的图片路径（.png 格式）
    :param confidence: 匹配精度（0~1）
    :param timeout: 超时时间（秒）
    :return: bool - 是否成功点击
    """
    print(f"正在查找图片: {image_path} (匹配精度: {confidence})")

    end_time = time.time() + timeout

    while time.time() < end_time:
        try:
            # === 关键修复：使用 pygetwindow 检查窗口是否还存在 ===
            all_titles = gw.getAllTitles()
            if window.title not in all_titles:
                print("目标窗口已关闭或不存在")
                return False

            # 获取窗口位置和大小
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
                return True

        except pyautogui.ImageNotFoundException:
            # 图像未找到，继续循环
            pass
        except Exception as e:
            # 打印异常但不停止循环
            print(f"❌ 查找图片时发生异常: {e}")
            time.sleep(0.5)

        time.sleep(0.5)  # 控制查找频率

    print(f"❌ 超时({timeout}s)：在窗口中未找到图片 {image_path}")
    return False