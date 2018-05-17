#!flask/bin/python3.6
# -*- coding: utf-8 -*-
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
from config1000.configs import USERVERIFYCODE_CONFIG


# phone_number是用户的电话号码。
def sing_sender(phone_number, verifycode):
    appid = USERVERIFYCODE_CONFIG['appid']
    appkey = USERVERIFYCODE_CONFIG['appkey']
    template_id = USERVERIFYCODE_CONFIG['template_id']
    params = [str(verifycode), str(USERVERIFYCODE_CONFIG['expirtime'])]
    ssender = SmsSingleSender(appid, appkey)
    try:
        result = ssender.send(0, 86, str(phone_number), "您的验证码是：" + str(verifycode) + "，请于" + str(
            USERVERIFYCODE_CONFIG['expirtime']) + "分钟内填写。如非本人操作，请忽略本短信。")
        return result
    except HTTPError as e:
        return e
    except Exception as e:
        return e
