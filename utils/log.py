import logging
from logging.handlers import RotatingFileHandler
import os


class SimpleLogger:
    def __init__(self, log_file='app.log', log_level=logging.DEBUG, max_bytes=5 * 1024 * 1024, backup_count=5):
        """
        初始化日志记录器

        :param log_file: 日志文件路径
        :param log_level: 日志级别（DEBUG, INFO, WARNING, ERROR, CRITICAL）
        :param max_bytes: 日志文件最大大小（字节）
        :param backup_count: 保留的日志文件数量
        """
        # 配置日志记录器
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

        # 配置文件处理器
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setLevel(log_level)

        # 配置日志格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # 将处理器添加到日志记录器
        self.logger.addHandler(file_handler)

    def debug(self, message):
        """记录调试信息"""
        self.logger.debug(message)

    def info(self, message):
        """记录普通信息"""
        self.logger.info(message)

    def warning(self, message):
        """记录警告信息"""
        self.logger.warning(message)

    def error(self, message):
        """记录错误信息"""
        self.logger.error(message)

    def critical(self, message):
        """记录严重错误信息"""
        self.logger.critical(message)


# 使用示例
if __name__ == "__main__":
    logger = SimpleLogger('logs/my_app.log', log_level=logging.INFO)

    logger.debug("这是一个调试信息")
    logger.info("这是一个普通信息")
    logger.warning("这是一个警告信息")
    logger.error("这是一个错误信息")
    logger.critical("这是一个严重错误信息")