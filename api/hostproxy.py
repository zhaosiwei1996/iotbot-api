from fastapi.encoders import jsonable_encoder
from fastapi import Header, APIRouter
from api.apidoc import *
from libs import utils, models
import logging

router = APIRouter()

# 获取主机代理信息(分页接口)


@router.get("/api/host/proxy", name="获取服务器代理数据", description="获取服务器代理数据(分页接口)", response_model=generalresp)
async def gethostpyoxylist(page: int, size: int, hostid: str = None, Authorization: str = Header(None)):
    logging.debug("get receive:/api/host/proxy?hostid=%s&page=%s&size=%s"%(hostid,page,size))
    if utils.check_token(Authorization):
        if hostid != '':
            return utils.sendjson(200, 'success', jsonable_encoder(await models.IotbotProxyTcpConfigs.filter(hostid=hostid)))
        else:
            try:
                datacount = await models.IotbotProxyTcpConfigs.all().count()
                querysql = jsonable_encoder(await models.IotbotProxyTcpConfigs.all().order_by('-serverport').limit(size).offset(int("%s%s" % (page-1, 0))))
            except Exception as ex:
                return utils.sendjson(500, '%s' % ex, [])
            else:
                return utils.sendjson(200, 'success', {'items': querysql, 'page': page, 'size': size, 'total': datacount})
    else:
        return utils.sendjson(401, 'token无效或错误', [])


# 获取主机代理信息(获取所有)
@router.get("/api/host/proxy/all", name="获取所有服务器代理数据", description="获取所有服务器代理数据", response_model=generalresp)
async def gethostlistall(Authorization: str = Header(None)):
    logging.debug("get receive:/api/host/proxy/all")
    if utils.check_token(Authorization):
        return utils.sendjson(200, 'success', jsonable_encoder(await models.IotbotProxyTcpConfigs.all().order_by('-serverport')))
    else:
        return utils.sendjson(401, 'token无效或错误', [])

# 主机代理添加


@router.put("/api/host/proxy", name="添加服务器代理数据", description="添加服务器代理数据", response_model=generalresp)
async def puthostpyoxylist(receive: addserverproxy, Authorization: str = Header(None)):
    tojson = jsonable_encoder(receive)
    logging.debug("put receive:/api/host/proxy json:%s"%tojson)
    if utils.check_token(Authorization):
        try:
            # 查询是否存在的hostid
            await models.IotbotProxyTcpConfigs.get(hostid=tojson['hostid'])
        except Exception as ex:
            try:
                # 查找最后一条serverport并+1,实现端口不重复
                selectport = await models.IotbotProxyTcpConfigs.all().order_by('-serverport').limit(1)
                for port in jsonable_encoder(selectport):
                    portadd = int(port['serverport'])+1
                await models.IotbotProxyTcpConfigs.create(hostid=tojson['hostid'], proxyname=tojson['proxyname'], targetaddr=tojson['proxyip'], serverport=portadd, mark=tojson['mark'], active=tojson['active'])
            except Exception as ex:
                logging.error(ex)
                return utils.sendjson(500, '数据添加失败:%s' % ex, [])
            else:
                return utils.sendjson(200, '主机代理添加成功', {"hostid": tojson['hostid']})
        else:
            try:
                # 数据存在的情况下,更新数据
                await models.IotbotProxyTcpConfigs.filter(hostid=tojson['hostid']).update(proxyname=tojson['proxyname'], targetaddr=tojson['proxyip'], mark=tojson['mark'], active=tojson['active'])
            except Exception as ex:
                logging.error(ex)
                return utils.sendjson(500, '数据已存在,但更新失败:%s' % ex, [])
            else:
                return utils.sendjson(200, '数据已存在,更新完成', {"hostid": tojson['hostid']})
    else:
        return utils.sendjson(401, 'token无效或错误', [])
