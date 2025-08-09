import ctypes

def run_as_admin(exe_path):
    """
    使用 ShellExecuteW 以管理员身份运行指定的 exe 文件
    :param exe_path: exe 文件路径（字符串）
    :return: 成功返回 True，否则返回 False
    """
    try:
        res = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", exe_path, None, None, 1)
        if res <= 32:
            print(f"启动失败，错误码: {res}")
            return False
        print(f"已请求以管理员身份运行: {exe_path}")
        return True
    except Exception as e:
        print(f"发生异常: {e}")
        return False

# import subprocess
import psutil
# import time
from vpn_open import *

def wait_for_process(process_name, timeout=40):
    """等待进程启动，超时返回False"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        for proc in psutil.process_iter(['name']):
            if process_name.lower() in proc.info['name'].lower():
                print(f"进程 {process_name} 已启动")
                return True
        time.sleep(1)  # 每秒检查一次
    print(f"等待超时，进程 {process_name} 未启动")
    return False

def open_process():
    # vpn_auto()
    vpn_auto_thread()
    if wait_for_process("EasyConnect.exe"):
        # 异步启动第二个程序（不阻塞）
        exe_path2 = r'"C:\Program Files (x86)\WN\Proxy4HisIns\ProxySvr4HIS.exe"'
        # subprocess.Popen(exe_path2)
        # wait_for_process("ProxySvr4HIS.exe")
        # if run_as_admin(exe_path2):
        #     if wait_for_process("ProxySvr4HIS.exe"):
        #         print("ProxySvr4HIS.exe 启动成功")
        #     else:
        #         print("等待 ProxySvr4HIS.exe 启动超时")
        # else:
        #     print("无法以管理员身份启动 ProxySvr4HIS.exe")
        run_as_admin(exe_path2)
        wait_for_process("ProxySvr4HIS.exe")
        # 异步启动第三个程序
        exe_path3 = r'"C:\Program Files\MountTaiSoftware\CLodop64\CLodopPrint64.exe"'
        subprocess.Popen(exe_path3)
        wait_for_process("CLodopPrint64.exe")
        # 链式调用 关闭窗口
        from prompt_verify import app_window
        import prompt_verify
        app_window.after(500, prompt_verify.show_completion_message)
    else:
        print("第一个程序启动失败，取消后续操作")