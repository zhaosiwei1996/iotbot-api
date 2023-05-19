from fastapi.encoders import jsonable_encoder
from fastapi import Header, APIRouter
from api.apidoc import *
from libs import utils, models
import logging

router = APIRouter()

# 主机列表(分页接口)


@router.get("/api/host/server", name="获取服务器数据", description="获取服务器数据(分页接口)", response_model=generalresp)
async def gethostlist(page: int, size: int, hostid: str = None, localip: str = None, Authorization: str = Header(None)):
    logging.info("get receive:/api/host/server?hostid=%s&localip=%s&page=%s&size=%s"%(hostid,localip,page,size))                                                
    if utils.check_token(Authorization):
        if hostid != '':
            return utils.sendjson(200, 'success', jsonable_encoder(await models.IotbotHeartbeats.filter(hostid=hostid)))
        elif localip != '':
            return utils.sendjson(200, 'success', jsonable_encoder(await models.IotbotHeartbeats.filter(localip=localip)))
        elif hostid or localip != '':
            return utils.sendjson(200, 'success', jsonable_encoder(await models.IotbotHeartbeats.filter(hostid=hostid, localip=localip)))
        else:
            try:
                datacount = await models.IotbotHeartbeats.all().count()
                querysql = jsonable_encoder(await models.IotbotHeartbeats.all().order_by('-createtime').limit(size).offset(int("%s%s" % (page-1, 0))))
            except Exception as ex:
                return utils.sendjson(500, "查询失败:%s" % ex, [])
            else:
                return utils.sendjson(200, 'success', {'items': querysql, 'page': page, 'size': size, 'total': datacount})
    else:
        return utils.sendjson(401, 'token无效或错误', [])

# 主机列表(获取所有)


@router.get("/api/host/server/all", name="获取所有服务器数据", description="获取所有服务器数据", response_model=generalresp)
async def gethostlistall(Authorization: str = Header(None)):
    logging.info("get receive:/api/host/server/all")
    if utils.check_token(Authorization):
        return utils.sendjson(200, 'success', jsonable_encoder(await models.IotbotHeartbeats.all().order_by('-createtime')))
    else:
        return utils.sendjson(401, 'token无效或错误', [])

# 主机修改

    
@router.put("/api/host/server", name="修改服务器数据", description="修改服务器数据", response_model=generalresp)
async def puthostlist(receive: updateserver, Authorization: str = Header(None)):
    tojson = jsonable_encoder(receive)
    logging.info("put receive:/api/host/server json:%s"%tojson)
    if utils.check_token(Authorization):
        try:
            await models.IotbotHeartbeats.filter(hostid=tojson['hostid']).update(uniqueid=tojson['uniqueid'], hostname=tojson['hostname'])
        except Exception as ex:
            return utils.sendjson(500, ex, [])
        else:
            return utils.sendjson(200, '修改成功', {"hostid": tojson['hostid']})
    else:
        return utils.sendjson(401, 'token无效或错误', [])
