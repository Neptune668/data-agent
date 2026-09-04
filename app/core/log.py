"""
日志管理的目标：

1.定制日志输出格式，控制输出级别

2.自动将日志保存到日志文件

3.设置日志文件的大小，超过会自动创建一个新的文件

4.指定日志文件的有效期，过期会自动删除文件

5.记录当前日志输出是哪个请求的ID
"""
import sys
import uuid
from pathlib import Path

from loguru import logger

from app.conf.app_config import app_config
from app.core.context import get_req_id

# 删除默认设置
logger.remove()

# 配置日志的格式
log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "  # 绿色显示日志时间（精确到毫秒）
    "<level>{level: <8}</level> | "  # 按级别颜色显示日志级别（左对齐，占8个字符）
    "<magenta>request_id - {extra[request_id]}</magenta> | "  # 品红色显示request_id（从日志extra中获取）
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "  # 青色显示日志所在文件、函数、行号
    "<level>{message}</level>"  # 按级别颜色显示日志正文
)

# 向日志输出注入请求ID
# 该函数由loguru在每次输出日志前调用
def inject_request_id(record):
    # 获取请求id
    request_id = get_req_id() # None
    if request_id == 'None':
        request_id = uuid.uuid4()
    record['extra']['request_id'] = request_id

# 给日志打补丁
logger = logger.patch(inject_request_id)

if app_config.logging.console.enable:
   # 添加控制台日志输出
   # sink = sys.stdout 日志在控制台输出
    logger.add(sink=sys.stdout, format=log_format, level=app_config.logging.console.level)

# 获取日志存储的路径
log_path = Path(__file__).parents[2]/'logs/app.log'

if app_config.logging.file.enable:
    # 添加日志文件输出
    logger.add(
        sink=log_path, # 日志文件路径
        format=log_format, # 输出格式
        level=app_config.logging.file.level, # 日志级别
        rotation=app_config.logging.file.rotation,  # 日志文件超过指定大小则创建新的日志文件
        retention=app_config.logging.file.retention,  # 日志文件有效期7天
        encoding='utf-8', # 日志文件编码
    )

if __name__ == '__main__':
    # 日志级别从低到高
    logger.debug('调试信息')
    logger.info('普通信息')
    logger.warning('警告信息')
    logger.error('错误信息')
    logger.critical('严重错误')
    # 上面的日志输出都有默认的设置
    # 要自定义输出格式，需要先删除默认设置
