import pyautogui
import time
import cv2
import numpy as np
import pygetwindow as gw

# 1. 查找目标窗口（替换为你实际要操作的窗口标题）
target_window_title = "Notepad"  # 示例：记事本
window = gw.getWindowsWithTitle(target_window_title)[0]

if window:
    # 2. 激活窗口（将其置于前台）
    window.activate()
    time.sleep(1)  # 等待窗口激活

    # 3. 截图整个屏幕或者指定区域
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 4. 加载你要点击的图标模板（请准备一张该图标的截图作为模板）
    template = cv2.imread('icon_template.png')  # 替换为你的图标模板图片路径

    # 5. 使用模板匹配查找图标位置
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(result >= threshold)

    # 6. 找到第一个匹配点并点击
    for pt in zip(*loc[::-1]):  # 取第一个匹配的位置
        center_x = pt[0] + template.shape[1] // 2
        center_y = pt[1] + template.shape[0] // 2

        print(f"找到图标，坐标：({center_x}, {center_y})")
        pyautogui.click(center_x, center_y)
        break
else:
    print("找不到目标窗口，请确认窗口标题是否正确。")

    '''启动脚本弹出密码，启动脚本弹出文本页面'''