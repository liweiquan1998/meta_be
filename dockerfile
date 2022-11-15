
FROM registry.cn-hangzhou.aliyuncs.com/sxtest/datax-admin:latest

COPY requirements.txt  /tmp/
WORKDIR /tmp
RUN /opt/conda/envs/py38/bin/pip install -r requirements.txt -i https://pypi.douban.com/simple/
RUN rm /etc/supervisor/conf.d/be.conf
CMD ["supervisord", "-n","-c", "/etc/supervisor/supervisord.conf" ]
