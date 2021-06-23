FROM iotcore-cn-north-1.jcr.service.jdcloud.com/baseimage/python3:latest
RUN mkdir -p /export/servers/iotbot-api
WORKDIR /export/servers/iotbot-api
ADD iotbot-api.py iotbot-api.py 
ADD setting setting 
ADD libs libs
ADD requirements.txt requirements.txt
RUN ls -al
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN rm -rf ~/.cache/pip
ENTRYPOINT python iotbot-api.py
