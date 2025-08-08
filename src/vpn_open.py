import os
import subprocess
import pyautogui
import time
import pygetwindow as gw
from identify import click_image_in_window

def vpn_auto():
    # 程序路径（注意路径中如果有空格，需要用双引号包裹）
    exe_path = r'"C:\Program Files (x86)\Sangfor\SSL\EasyConnect\EasyConnect.exe"'
    # 启动图形化程序
    subprocess.Popen(exe_path)
    # time.sleep(6)
    # # 查找目标窗口（根据标题）
    # target_window = gw.getWindowsWithTitle("EasyConnect")[0]
    # 增加等待时间并循环查找窗口
    max_attempts = 10  # 最多尝试15次
    for attempt in range(max_attempts):
        time.sleep(1)  # 每次等待1秒
        windows = gw.getWindowsWithTitle("EasyConnect")
        if windows:
            target_window = windows[0]
            print(f"在尝试 {attempt + 1} 时找到窗口")
            break
        else:
            print(f"尝试 {attempt + 1}/{max_attempts}: 未找到EasyConnect窗口")
    else:
        # 循环结束仍未找到窗口
        print("错误：启动后无法找到EasyConnect窗口")
        print("当前所有可见窗口：")
        for window in gw.getWindowsWithTitle(""):
            if window.visible:
                print(f"- {window.title}")
        return None  # 或者抛出异常
    print("EasyConnect 已启动")

    if target_window:
        target_window.activate()
        login_img_path = os.path.abspath("../assets/images/login.PNG")
        found_login = click_image_in_window(target_window, login_img_path)
        # 根据返回结果判断是否执行后续操作
        if found_login:
            print("图片已找到并点击")
        else:
            print("图片未找到，执行备用方案")
            time.sleep(14)
            # 地址界面跳转
            for _ in range(2):
                pyautogui.press('tab')
                time.sleep(0.3)
                pyautogui.press('enter')
            # 登录界面跳转 可以升级为按图片检测
            time.sleep(5.5)
            for _ in range(6):
                pyautogui.press('tab')
                time.sleep(0.3)
            pyautogui.press('enter')
    else:
        print("找不到目标窗口，请确认标题是否正确。")
