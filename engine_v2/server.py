import json

from flask import Flask, g, jsonify
from loguru import logger

import settings
from storages.get_storage import DEFAULT_STORAGE_CLASS
from storages.redis_storage import RedisStorage
from utils.log import SimpleLogger
from panda_python_kit.comm.result_model import ResultModel

app = Flask(__name__)
logger = SimpleLogger(log_file=settings.SERVER_LOG_PATH)


@app.route("/")
def hello_world():
    return ("""
     "<p>welcom to scrapy proxy pool system !</p>
      <li><a href="/get_proxy">/get_proxy<a></li>
      <li><a href="/get_all">/get_all<a></li>
    
    """)


@app.route("/get_proxy")
def get_proxy():
    conn = get_conn()
    proxy = conn.random()
    # 如果抛出异常，返回错误信息
    if not proxy:
        return jsonify(ResultModel(data=None, success=False, message="no proxy").to_dict())
    return jsonify(ResultModel(data=proxy).to_dict())
# @app.route("/get_all")
# def get_all():
#     conn = get_conn()
#     proxies = conn.all()
#     return proxies.to_json()

@app.route("/count")
def get_count():
    conn = get_conn()
    return jsonify(ResultModel(data=conn.count()).to_dict())

def get_conn():
    if not hasattr(g,'conn'):
        g.conn = DEFAULT_STORAGE_CLASS.get_client_from_config()
        return g.conn


if __name__ == '__main__':
    logger.info("server start")
    app.run(host=settings.SERVER_HOST, port=settings.SERVER_PORT, threaded=settings.SERVER_THREAD,logger=logger,debug=True)
    logger.info("server end")