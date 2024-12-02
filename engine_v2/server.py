import json

from flask import Flask,g
from loguru import logger

import settings
from storages.get_storage import DEFAULT_STORAGE_CLASS
from storages.redis_storage import RedisStorage
from utils.log import SimpleLogger

app = Flask(__name__)
logger = SimpleLogger(log_file=settings.SERVER_LOG_PATH)


@app.route("/")
def hello_world():
    return ("""
     "<p>welcom to scrapy proxy pool system !</p>
     <li>/get_proxy</li>
     <li>/get_all</li>
    
    """)


@app.route("/get_proxy")
def get_proxy():
    conn = get_conn()
    proxy = conn.random()
    return  proxy.to_json()

# @app.route("/get_all")
# def get_all():
#     conn = get_conn()
#     proxies = conn.all()
#     return proxies.to_json()

@app.route("/count")
def get_count():
    conn = get_conn()
    return {"count": conn.count()}
def get_conn():
    if not hasattr(g,'conn'):
        g.conn = DEFAULT_STORAGE_CLASS.get_client_from_config()
        return g.conn


if __name__ == '__main__':
    app.run(host=settings.SERVER_HOST, port=settings.SERVER_PORT, threaded=settings.SERVER_THREAD,logger=logger)