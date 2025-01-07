import json

from flask import Flask, g, jsonify,request
from loguru import logger
from panda_python_kit.comm.comm import get_request_data

import settings
from storages.get_storage import DEFAULT_STORAGE_CLASS
from storages.redis_storage import RedisStorage
from utils.log import SimpleLogger
from panda_python_kit.comm.result_model import ResultModel

# from utils.proxy import extract_auth_proxy

app = Flask(__name__)
logger = SimpleLogger(log_file=settings.SERVER_LOG_PATH)


@app.route("/")
def hello_world():
    return ("""
     "<p>welcome to scrapy proxy pool system !</p>
      <li><a href="/get_one">/get_one<a></li>
      <li><a href="/pop_one">/pop_one<a></li>
      <li><a href="/get_all">/get_all<a></li>
      <li><a href="/count">/count<a></li>
    
    """)


@app.route("/get_one")
def get_one():
    conn = get_conn()
    proxy = conn.random()
    # 如果抛出异常，返回错误信息
    if not proxy:
        return jsonify(ResultModel(data=None, success=False, message="no proxy").to_dict())
    return jsonify(ResultModel(data=proxy).to_dict())

@app.route("/pop_one")
def pop_one():
    conn = get_conn()
    proxy= get_request_data(request=request).get("proxy")
    remove_result = conn.remove(extract_auth_proxy(proxy))
    if remove_result:
        return jsonify(ResultModel(data=proxy).to_dict())
    return jsonify(ResultModel(data=proxy,success=False,message="proxy 不存在").to_dict())



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