import subprocess
import pyautogui
import time
import pygetwindow as gw
import threading
from identify import click_image_in_window, resource_path


def vpn_auto_thread():
    try:
        # 启动程序
        exe_path = r'"C:\Program Files (x86)\Sangfor\SSL\EasyConnect\EasyConnect.exe"'
        subprocess.Popen(exe_path)
        # target_window = gw.getWindowsWithTitle("EasyConnect")[0]
        # 增加等待时间并循环查找窗口
        max_attempts = 10  # 最多尝试15次
        # 查找窗口
        target_window = None
        for attempt in range(max_attempts):
            windows = gw.getWindowsWithTitle("EasyConnect")
            if windows:
                target_window = windows[0]
                print(f"在尝试 {attempt + 1} 时找到窗口")
                break
            print(f"尝试 {attempt + 1}/10: 未找到EasyConnect窗口")
            time.sleep(1)

        if not target_window:
            raise Exception("无法找到EasyConnect窗口")

        print("EasyConnect 已启动")
        # 激活窗口
        target_window.activate()
        # 图片路径
        # link_img_path = os.path.abspath("../assets/images/button.png")
        # login_img_path = os.path.abspath("../assets/images/login.png")
        link_img_path = resource_path("assets/images/button.png")
        login_img_path = resource_path("assets/images/login.png")
        # 查找图片
        found_button = False
        found_login = False
        start_time = time.time()
        max_attempts = 3  # 最大重试次数
        link_click_count = 0  # 链接图片点击计数器

        while time.time() - start_time < 30 and not found_login:
            # 动态处理链接图片（允许重复点击）
            if link_click_count < max_attempts:  # 限制最大点击次数
                if click_image_in_window(target_window, link_img_path, timeout=1):
                    print("链接图片已找到并点击")
                    link_click_count += 1
                    time.sleep(1)  # 点击后短暂等待页面响应

            # 检查登录图片
            if click_image_in_window(target_window, login_img_path, timeout=1):
                print("登录图片已找到并点击")
                found_login = True
                break
            else:
                # 如果登录图片未出现，重置链接点击计数器（允许重新尝试）
                if link_click_count >= max_attempts:
                    print("达到最大链接点击次数，重置计数器")
                    link_click_count = 0
        if not found_login:
            print("登录图片未找到，执行备用方案")
            time.sleep(1)
            for _ in range(6):
                pyautogui.press('tab')
                time.sleep(0.3)
            pyautogui.press('enter')

    except Exception as e:
        print(f"VPN自动化过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


def open_process():
    thread = threading.Thread(target=vpn_auto_thread)
    thread.daemon = True
    thread.start()
