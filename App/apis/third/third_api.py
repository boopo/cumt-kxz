import logging

from flask_restful import reqparse, Resource

from App.apis.third.third_utils import token_generator, ThirdIds, t_check_captcha
from App.ext import redis_third

parse_third = reqparse.RequestParser()
parse_third.add_argument("username", type=str, help='请输入学号', required=True, location=['json'])
parse_third.add_argument("password", type=str, help='请输入密码', required=True, location=['json'])
parse_third.add_argument("extra", type=str, help='请输入选项', required=True, location=['json'])

parse_captcha = reqparse.RequestParser()
parse_captcha.add_argument("")


# 写的有亿点点乱，但毕竟特殊情况嘛
class ThirdPartyLogin(Resource):
    def post(self):
        try:
            args = parse_third.parse_args()
            username = args.get('username')
            password = args.get('password')
            extra = args.get('extra')
            if t_check_captcha(username):
                p_id = ThirdIds(username, password)
                if p_id.login_pro():
                    pro_token = token_generator(username, password)
                    redis_third.set(name=username, value=pro_token)
                    if 'true' in extra:
                        _l1 = p_id.get_self_info()
                        d1 = {
                            "name": _l1[0],
                            "college": _l1[1],
                            "classname": _l1[3],
                            "sex": _l1[4]
                        }
                        return {
                            "msg": "登陆成功",
                            "data": d1,
                            "token": pro_token
                        }
                    else:
                        return {
                                   "msg": "登陆成功，验证码已自动为您填写",
                                   "data": '',
                                   "token": pro_token
                               }
                else:
                    return {
                        "msg": "登陆失败,你的密码可能大概也许真的输错了",
                        'data': '',
                        "token": ''
                    }, 401
            id = ThirdIds(username, password)
            if id.login():
                _token = token_generator(username, password)
                redis_third.set(name=username, value=_token)

                if 'true' in extra:  # 2s
                    l1 = id.get_self_info()
                    d1 = {
                        "name": l1[0],
                        "college": l1[1],
                        "classname": l1[3],
                        "sex": l1[4]
                    }
                    return {
                        "msg": "登陆成功",
                        "data": d1,
                        "token": _token
                    }
                else:  # 700ms
                    return {
                        "msg": "登陆成功",
                        'data': '',
                        "token": _token
                    }
            else:
                return {
                           "msg": "用户名或密码错误",
                           'data': '',
                           "token": ""
                       }, 401
        except Exception as e:
            logging.info(e)
        return {
                   "msg": "认证失败，请重试",
                   "data": "",
                   "token": ''
               }, 500


'''
class LoginCaptcha(Resource):
    def get(self):
        try:
            args = parse_captcha.parse_args()
            username = args.get('username')
            password = args.get('password')
            captcha = args.get('captcha')
            return {
                "msg": "test"
            }
        except Exception as e:
            print(e)
            return {
               "msg": "error"
            }
'''
