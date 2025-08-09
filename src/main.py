import tkinter as tk
import logger_config
import check_launch
import prompt_verify  # 你的密码窗口模块

if __name__ == "__main__":
    # 1. 初始化日志
    logger_config.setup_logger()

    # 2. 初始化唯一的 Tkinter 主窗口（隐藏，作为所有子窗口的容器）
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口，不显示界面

    # 3. 定义主流程函数（将检查逻辑放入主循环任务队列）
    def main_process():
        if check_launch.check_launch_limit():
            prompt_verify.show_password_window()
    # 4. 将主流程放入主循环的任务队列（确保在主循环启动后执行）
    root.after(0, main_process)
    # 5. 启动主事件循环（此时才会处理窗口创建和渲染）
    root.mainloop()