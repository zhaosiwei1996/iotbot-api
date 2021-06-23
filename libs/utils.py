from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from fastapi.responses import JSONResponse
from setting import config
import logging
import time
logging.basicConfig(level=config.logging_level, format='[%(levelname)s] %(asctime)s [%(funcName)s] %(message)s')
logger = logging.getLogger(__name__)
    
#token检查
def check_token(token):
    try:
        usertoken = Serializer(config.SECRET_KEY,config.ACCESS_TOKEN_EXPIRE_MINUTES).loads(token)
    except Exception as ex:
        logging.error('token校验失败,%s'%ex)
        return False
    else:
        logging.info('token校验成功,%s'%usertoken)
        return True

#统一json返回格式
def jsonresp(httpcode, msg, data):
    resp = {"rescode": httpcode, "msg": msg,'timestamp':time.time(),"data": data}
    logging.info("返回结果:%s"%resp)
    return JSONResponse(status_code=httpcode,content=resp)