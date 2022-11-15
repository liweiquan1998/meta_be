
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s| \"%(pathname)s\", line %(lineno)d,\n %(levelname)s: %(message)s"
)
ch.setFormatter(formatter)
logger.addHandler(ch) #将日志输出至屏幕