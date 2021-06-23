from tortoise.models import Model
from tortoise import fields

class IotbotHeartbeats(Model):
    hostname = fields.CharField(max_length=50)
    vermajor = fields.IntField()
    verminor = fields.IntField()
    statuscode = fields.IntField()
    createtime = fields.DatetimeField()
    hbtime = fields.DatetimeField()
    localip = fields.CharField(max_length=50)
    publicip = fields.CharField(max_length=50, blank=True, null=True)
    platform = fields.CharField(max_length=50, blank=True, null=True)
    uniqueid = fields.CharField(max_length=50, blank=True, null=True)
    hostid = fields.CharField(unique=True, max_length=60, blank=True, null=True)

    class Meta:
        table = 'iotbot_heartbeats'


class IotbotProxyTcpConfigs(Model):
    hostid = fields.CharField(max_length=100)
    proxyname = fields.CharField(unique=True, max_length=20)
    targetaddr = fields.CharField(max_length=200)
    serverport = fields.CharField(unique=True, max_length=10)
    mark = fields.CharField(max_length=200)
    active = fields.IntField()

    class Meta:
        table = 'iotbot_proxy_tcp_configs'


class IotbotSyncConfigs(Model):
    filename = fields.CharField(max_length=100)
    filedata = fields.TextField()
    owneruser = fields.CharField(max_length=20)
    ownergroup = fields.CharField(max_length=20)
    filepath = fields.CharField(max_length=100)
    mask = fields.CharField(max_length=11)
    active = fields.IntField()

    class Meta:
        table = 'iotbot_sync_configs'

class IotbotUserList(Model):
    user_name = fields.CharField(max_length=100)
    user_fullname = fields.CharField(max_length=100)
    user_password = fields.CharField(max_length=100)
    create_time = fields.DatetimeField()
    update_time = fields.DatetimeField()

    class Meta:
        table = 'iotbot_user_list'

class IotbotApiUserList(Model):
    username = fields.CharField(max_length=100)
    userfullname = fields.CharField(max_length=100)
    userpassword = fields.CharField(max_length=100)
    createtime = fields.DatetimeField()
    updatetime = fields.DatetimeField()

    class Meta:
        table = 'iotbot_api_user_list'