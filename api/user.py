from itsdangerous import TimestampSigner as Serializer
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from api.apidoc import *
from libs import utils, models
from setting import config
import ujson as json
import requests
import logging

router = APIRouter()

# 用户登录

@router.get("/")
async def testapi():
    return utils.sendjson(200,"hello world",[])

@router.post("/api/user", name="用户登录获取token", description="使用erp账号登陆并获取token", response_model=generalresp)
async def userlogin(receive: userlogin):
    tojson = jsonable_encoder(receive)
    logging.info('post receive:/api/user json:%s' % tojson)
    jdssocheck = json.loads(requests.post(
        url=config.jdsso, data=tojson).text)
    logging.info('sso resp:%s' % jdssocheck)
    if jdssocheck['REQ_CODE'] == 11:
        return utils.sendjson(403, 'erp用户名或密码不正确', [])
    elif jdssocheck['REQ_CODE'] == 1:
        getusertoken = await models.IotbotApiUserList.filter(username=jdssocheck['REQ_DATA']['username'])
        if getusertoken == None:
            return utils.sendjson(403, '没有权限,请联系iot运维组开通', [])
        else:
            accesstoken = Serializer(config.SECRET_KEY, config.ACCESS_TOKEN_EXPIRE_MINUTES).dumps(
                {'username': jdssocheck['REQ_DATA']['username'], 'orgname': jdssocheck['REQ_DATA']['orgName']}).decode()
            return utils.sendjson(200, '登陆成功', {'username': jdssocheck['REQ_DATA']['username'], 'fullname': jdssocheck['REQ_DATA']['fullname'], 'token': '%s' % accesstoken})
    elif jdssocheck['REQ_CODE'] == 12:
        return utils.sendjson(403, jdssocheck['REQ_MSG'], [])
    else:
        return utils.sendjson(403, jdssocheck['REQ_MSG'], [])
