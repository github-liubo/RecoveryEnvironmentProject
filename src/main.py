# 主程序入口

# 第一步：导入日志配置，触发print重定向
import logger_config
import prompt_verify
if __name__ == "__main__":
    logger_config.setup_logger()
    prompt_verify.show_password_window()  # 程序入口：先显示密码窗口
