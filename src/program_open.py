

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
    vpn_auto()
    if wait_for_process("EasyConnect.exe"):
        # 异步启动第二个程序（不阻塞）
        exe_path2 = r'"C:\Program Files (x86)\WN\Proxy4HisIns\ProxySvr4HIS.exe"'
        subprocess.Popen(exe_path2)
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