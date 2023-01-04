# -*- coding: utf-8 -*-
import multiprocessing
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent.parent

debug = False

# ============================================================
# gunicorn要切换到的目的工作目录
# ============================================================

chdir = str(BASE_DIR)

# ============================================================
# server socket相关
# ============================================================

# 指定绑定的ip和端口
bind = "0.0.0.0:8000"

# 服务器中排队等待的最大连接数，建议值64-2048，超过2048时client连接会得到一个error
backlog = 2048

# ============================================================
# 调试相关
# ============================================================

# 当代码有修改时，自动重启workers，适用于开发环境
reload = False

# 以守护进程形式来运行Gunicorn进程，其实就是将这个服务放到后台去运行
daemon = False

# ============================================================
# worker进程相关
# ============================================================

# 用于处理工作的进程数
workers = multiprocessing.cpu_count() * 2 + 1

# worker进程的工作方式，有sync、eventlet、gevent、tornado、gthread, 默认是sync,
# django使用gevent容易造成阻塞, 使用gthread的方式好一些
worker_class = 'gthread'

# 指定每个工作进程开启的线程数
threads = multiprocessing.cpu_count() * 2

# 访问超时时间
timeout = 30

# 接收到restart信号后，worker可以在graceful_timeout时间内，继续处理完当前requests
graceful_timeout = 60

# server端保持连接时间
keepalive = 30

# ============================================================
# 日志相关
# ============================================================

"""日志文件格式，其每个选项的含义如下：
h          remote address
l          '-'
u          currently '-', may be user name in future releases
t          date of the request
r          status line (e.g. ``GET / HTTP/1.1``)
s          status
b          response length or '-'
f          referer
a          user agent
T          request time in seconds
D          request time in microseconds
L          request time in decimal seconds
p          process ID
"""
access_log_format = '%(t)s %(h)s "%(r)s" %(s)s %(b)s "%(f)s" "%(L)s"'

LOG_DIR = Path(BASE_DIR, 'log')
if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True)

# 错误日志输出等级，访问日志的输出等级无法设置
loglevel = "error"

# 正常的日志文件路径，'-'表示输出到终端
accesslog = '-'

# 错误日志文件路径，'-'表示输出到终端
errorlog = str(LOG_DIR / 'gunicorn_error.log')

# ============================================================
# 进程名相关
# ============================================================

# 设置进程名称，默认是gunicorn
proc_name = 'gunicorn'
