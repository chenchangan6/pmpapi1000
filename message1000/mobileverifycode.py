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
    ssender = SmsSingleSender(appid, appkey)
    params = [str(verifycode), str(USERVERIFYCODE_CONFIG['expirtime'])]
    try:
        result = ssender.send(0, 86, phone_number, template_id, params)
        return result
    except HTTPError as e:
        return {'code': '500', 'message': 'HTTPError.', 'error': e}
    except Exception as e:
        return {'code': '500', 'message': 'SendError.', 'error': e}
