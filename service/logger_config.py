# 日志配置
import logging
import time

logger = logging.getLogger()
# logger.propagate = False  # 禁止向上传播
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s",
)
# 输出到控制台
to_console = logging.StreamHandler()
to_console.setFormatter(formatter)
logger.addHandler(to_console)

# 输出到文件中
to_file = logging.FileHandler(filename="log.txt")
to_file.setFormatter(formatter)
logger.addHandler(to_file)
