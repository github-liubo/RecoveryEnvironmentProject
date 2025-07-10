import psutil
import time

def close_process_by_name(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.name() and process_name.lower() in proc.name().lower():
                print(f"正在关闭进程: {proc.name()} (PID: {proc.pid})")
                p = psutil.Process(proc.pid)
                p.terminate()  # 发送终止信号
                p.wait(timeout=3)  # 等待最多3秒确认关闭
                print(f"程序{process_name}关闭成功")
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            print(f"无法关闭进程: {e}")

# 关闭vpn守护进程
def is_process_running(process_name):
    """检查指定名称的进程是否正在运行"""
    for proc in psutil.process_iter(['name']):
        if process_name.lower() in proc.info['name'].lower():
            return True
    return False

def close_program():
    # 第一个要关闭的程序
    close_process_by_name("ProxySvr4HIS.exe")
    # 第二个要关闭的程序
    close_process_by_name("CLodopPrint64.exe")
    if is_process_running("SangforCSClient"):
        close_process_by_name("SangforCSClient.exe")
    # 第三个要关闭的程序
    close_process_by_name("EasyConnect.exe")
    # 链式调用 打开多个程序
    from prompt_verify import app_window
    import program_open
    app_window.after(500, program_open.open_process)