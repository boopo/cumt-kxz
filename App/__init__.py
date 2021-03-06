import redis
from flask import Flask
from flask_cors import CORS


from App._settings import envs, Redis_local
from App.apis import init_api
from App.celery import celery_app
from App.ext import init_ext, db

from App.views import init_view
from logs.logs import setup_log


def create_app(env):
    app = Flask(__name__)
    # 跨域设置
    CORS(app, supports_credentials=True, origns="*")
    # 初始化配置
    app.config.from_object(envs.get(env))
    # 初始化API
    init_api(app)
    # 初始化View
    init_view(app)
    # 初始化第三方扩展
    init_ext(app)
    # 日志记录
    setup_log()
    # celery 暂停使用
    # celery_app.conf.update({
    #     "broker_url": Redis_local,
    #     "result_backend": Redis_local
    # })

    return app
