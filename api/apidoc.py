from pydantic import BaseModel
#post
class userlogin(BaseModel):
    username: str
    password: str

class updateserver(BaseModel):
    hostname: str
    hostid: str
    uniqueid: str

class addserverproxy(BaseModel):
    active: int
    hostid: str
    mark: str
    proxyip: str
    proxyname: str

# get resp
class generalresp(BaseModel):
    rescode: int
    msg: str 
    timestamp: int
    data: list