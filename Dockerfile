FROM python
USER root
VOLUME /data
WORKDIR /data
COPY ./requirements.txt /data/requirements.txt

RUN cd /data && \
    pip3 install --upgrade pip && \
    pip3 install -r /data/requirements.txt && \
	ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

CMD /bin/bash -c 'pytest ./TestCase --alluredir=Results'