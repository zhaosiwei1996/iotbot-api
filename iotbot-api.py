from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from tortoise.contrib.fastapi import register_tortoise
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, Header
from libs.apidoc import *
from libs import utils,models
from setting import config
import ujson as json
import multiprocessing
import requests
import logging
import uvicorn

logging.basicConfig(level=config.logging_level, format='[%(levelname)s] %(asctime)s [%(funcName)s] %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(debug=config.uvicorn_debug,docs_url='/api/docs',openapi_url='/api/openapi.json',redoc_url='/api/redoc')
#Mysql初始化
register_tortoise(app,db_url=config.db_url,modules={"models": ["libs.models"]},add_exception_handlers=True)

#api测试
@app.get("/api",name="默认uri", description="默认uri",response_model=generalresp)
def default():
    return utils.jsonresp(200,'hello world',[])

#用户登录
@app.post("/api/user",name="用户登录获取token", description="使用erp账号登陆并获取token",response_model=generalresp)
async def userlogin(receive: userlogin):
    logging.info('post receive:%s'%jsonable_encoder(receive))
    jdssocheck = json.loads(requests.post(url=config.jdsso, data=jsonable_encoder(receive)).text)
    logging.info('sso resp:%s'%jdssocheck)
    if jdssocheck['REQ_CODE'] == 11:
        return utils.jsonresp(403, 'erp用户名或密码不正确', [])
    elif jdssocheck['REQ_CODE'] == 1:
        getusertoken = await models.IotbotApiUserList.filter(username=jdssocheck['REQ_DATA']['username'])
        if getusertoken == None:
            return utils.jsonresp(403, '没有权限,请联系iot运维组开通', [])
        else: 
            accesstoken=Serializer(config.SECRET_KEY,config.ACCESS_TOKEN_EXPIRE_MINUTES).dumps({'username':jdssocheck['REQ_DATA']['username'],'orgname':jdssocheck['REQ_DATA']['orgName']}).decode()
            return utils.jsonresp(200, '登陆成功', {'username': jdssocheck['REQ_DATA']['username'], 'fullname': jdssocheck['REQ_DATA']['fullname'], 'token':'%s'%accesstoken})
    elif jdssocheck['REQ_CODE'] == 12:
        return utils.jsonresp(403, jdssocheck['REQ_MSG'], [])
    else:
        return utils.jsonresp(403, jdssocheck['REQ_MSG'], [])

#主机列表(分页接口)
@app.get("/api/host/server",name="获取服务器数据", description="获取服务器数据(分页接口)",response_model=generalresp)
async def gethostlist(page:int,size:int,hostid:str=None,localip:str=None,Authorization: str = Header(None)):
    if utils.check_token(Authorization):
        if hostid!='':
            return utils.jsonresp(200,'success',jsonable_encoder(await models.IotbotHeartbeats.filter(hostid=hostid)))
        elif localip!='':
            return utils.jsonresp(200,'success',jsonable_encoder(await models.IotbotHeartbeats.filter(localip=localip)))
        elif hostid or localip!='':
            return utils.jsonresp(200,'success',jsonable_encoder(await models.IotbotHeartbeats.filter(hostid=hostid,localip=localip)))
        else:
            try:
                datacount = await models.IotbotHeartbeats.all().count()
                querysql = jsonable_encoder(await models.IotbotHeartbeats.all().order_by('-createtime').limit(size).offset(int("%s%s"%(page-1,0))))
            except Exception as ex:
                return utils.jsonresp(500,"查询失败:%s"%ex,[])
            else:
                return utils.jsonresp(200,'success',{'items':querysql,'page':page,'size':size,'total':datacount})
    else:   
        return utils.jsonresp(401,'token无效或错误',[])

#主机列表(获取所有)
@app.get("/api/host/server/all",name="获取所有服务器数据", description="获取所有服务器数据",response_model=generalresp)
async def gethostlistall(Authorization: str = Header(None)):
    if utils.check_token(Authorization):
        return utils.jsonresp(200,'success',jsonable_encoder(await models.IotbotHeartbeats.all().order_by('-createtime')))
    else:
        return utils.jsonresp(401,'token无效或错误',[])

#主机修改
@app.put("/api/host/server",name="修改服务器数据", description="修改服务器数据",response_model=generalresp)
async def puthostlist(receive: updateserver,Authorization: str = Header(None)):
    if utils.check_token(Authorization):
        tojson = jsonable_encoder(receive)
        logging.info('put receive:%s'%tojson)
        try:
            await models.IotbotHeartbeats.filter(hostid=tojson['hostid']).update(uniqueid=tojson['uniqueid'], hostname=tojson['hostname'])
        except Exception as ex:
            return utils.jsonresp(500, ex, [])
        else:
            return utils.jsonresp(200, '修改成功', {"hostid": tojson['hostid']})
    else:
        return utils.jsonresp(401,'token无效或错误',[])

#获取主机代理信息(分页接口)
@app.get("/api/host/proxy",name="获取服务器代理数据", description="获取服务器代理数据(分页接口)",response_model=generalresp)
async def gethostpyoxylist(page:int,size:int,hostid:str=None,Authorization: str = Header(None)):
    if utils.check_token(Authorization):
        if hostid!='':
            return utils.jsonresp(200,'success',jsonable_encoder(await models.IotbotProxyTcpConfigs.filter(hostid=hostid)))
        else:
            try:
                datacount = await models.IotbotProxyTcpConfigs.all().count()
                querysql = jsonable_encoder(await models.IotbotProxyTcpConfigs.all().order_by('-serverport').limit(size).offset(int("%s%s"%(page-1,0))))
            except Exception as ex:
                return utils.jsonresp(500,'%s'%ex,[])
            else:
                return utils.jsonresp(200,'success',{'items':querysql,'page':page,'size':size,'total':datacount})
    else:
         return utils.jsonresp(401,'token无效或错误',[])


#获取主机代理信息(获取所有)
@app.get("/api/host/proxy/all",name="获取所有服务器代理数据", description="获取所有服务器代理数据",response_model=generalresp)
async def gethostlistall(Authorization: str = Header(None)):
    if utils.check_token(Authorization):
        return utils.jsonresp(200,'success',jsonable_encoder(await models.IotbotProxyTcpConfigs.all().order_by('-serverport')))
    else:
        return utils.jsonresp(401,'token无效或错误',[])

#主机代理添加
@app.put("/api/host/proxy",name="添加服务器代理数据", description="添加服务器代理数据",response_model=generalresp)
async def puthostpyoxylist(receive: addserverproxy, Authorization: str = Header(None)):
    if utils.check_token(Authorization):
        tojson = jsonable_encoder(receive)
        logging.info('put receive:%s'%tojson)
        try:         
            #查询是否存在的hostid
            await models.IotbotProxyTcpConfigs.get(hostid=tojson['hostid'])
        except Exception as ex:
            try:
                #查找最后一条serverport并+1,实现端口不重复
                selectport = await models.IotbotProxyTcpConfigs.all().order_by('-serverport').limit(1)
                for port in jsonable_encoder(selectport):
                    portadd = int(port['serverport'])+1
                await models.IotbotProxyTcpConfigs.create(hostid=tojson['hostid'],proxyname=tojson['proxyname'],targetaddr=tojson['proxyip'],serverport=portadd,mark=tojson['mark'],active=tojson['active'])
            except Exception as ex:
                logging.error(ex)
                return utils.jsonresp(500,'数据添加失败:%s'%ex,[])
            else:
                return utils.jsonresp(200, '主机代理添加成功', {"hostid": tojson['hostid']})
        else:
            try:
                #数据存在的情况下,更新数据
                await models.IotbotProxyTcpConfigs.filter(hostid=tojson['hostid']).update(proxyname=tojson['proxyname'],targetaddr=tojson['proxyip'],mark=tojson['mark'],active=tojson['active'])
            except Exception as ex:
                logging.error(ex)
                return utils.jsonresp(500,'数据已存在,但更新失败:%s'%ex,[])
            else:   
                return utils.jsonresp(200,'数据已存在,更新完成', {"hostid": tojson['hostid']})
    else:
        return utils.jsonresp(401,'token无效或错误',[])

if __name__ == '__main__':
    uvicorn.run(app='iotbot-api:app', host=config.uvicorn_host, port=config.uvicorn_port, reload=config.uvicorn_reload, debug=config.uvicorn_debug, workers=int(multiprocessing.cpu_count()))
