import logging
import platform
import os
import logging

#token加密
SECRET_KEY='%890@^85-k#f=o%s++&^x&5(zxtc=7sanme9ls2hmr(ext*@a9'
ACCESS_TOKEN_EXPIRE_MINUTES = 86400

#单点登录认证
jdsso='http://ssa.jd.com/sso/verify'

#根据系统类型进行环境匹配
if platform.system().lower() == 'windows':
    db_url='mysql://iotbot:Jdiot!23@mysql-cn-north-1-c193b0969c5c45c4.rds.jdcloud.com:3306/jd_iotbot'
    uvicorn_host='0.0.0.0'
    uvicorn_port=8000
    uvicorn_debug=True
    uvicorn_reload=True
    logging_level=logging.DEBUG

elif platform.system().lower() == 'linux':
    dbname =  os.environ.get('DB_NAME'),
    dbuser =  os.environ.get('DB_USERNAME'),
    dbpassword = os.environ.get('DB_PASSWORD'),
    dbhost = os.environ.get('DB_HOST'),
    dbport = os.environ.get('DB_PORT'),
    db_url = 'mysql://'+dbuser+dbpassword+'@'+dbhost+':'+dbport+'/'+dbname
    uvicorn_host = os.environ.get('UVICRON_HOST')
    uvicorn_port = os.environ.get('UVICRON_PORT')
    uvicorn_reload = False
    if os.environ.get('UVICRON_DEBUG')=='on':
        uvicorn_debug = True
    else:
        uvicorn_debug = False
    if os.environ.get('LOG_LEVEL')=='debug':
        logging_level= logging.DEBUG
    else:
        logging_level= logging.INFO
