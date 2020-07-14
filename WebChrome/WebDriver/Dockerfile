FROM dorowu/ubuntu-desktop-lxde-vnc:bionic

# Expose Macaca and VNC ports
EXPOSE 80
EXPOSE 5900

VOLUME /data
WORKDIR /data

ENV DEBIAN_FRONTEND=noninteractive

COPY sources.list /etc/apt/sources.list

RUN apt-get update --fix-missing && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN ( sleep 4 && while [ 1 ]; do sleep 1; echo y; done ) | apt-get install -y --no-install-recommends curl git openjdk-8-jdk fonts-droid-fallback ttf-wqy-zenhei ttf-wqy-microhei fonts-arphic-ukai fonts-arphic-uming fonts-tlwg-garuda
RUN ( sleep 4 && while [ 1 ]; do sleep 1; echo y; done ) | apt-get install -y --no-install-recommends vim zip unzip wget libappindicator3-1 language-pack-zh-han* fonts-liberation

RUN curl -o google-chrome-stable_current_amd64.deb -L https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb && rm -f google-chrome-stable_current_amd64.deb && apt-get autoremove -y && apt-get clean -y && \
    curl -o /opt/selenium-server-standalone.jar -L https://npm.taobao.org/mirrors/selenium/3.141/selenium-server-standalone-3.141.59.jar

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64 \
    JRE_HOME=${JAVA_HOME}/jre \
    CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib \
    PATH=${JAVA_HOME}/bin:$PATH

ENV NODE_VERSION=11.3.0 \
    NODE_REGISTRY=https://npm.taobao.org/mirrors/node

RUN curl -SLO "$NODE_REGISTRY/v$NODE_VERSION/node-v$NODE_VERSION-linux-x64.tar.gz" && \
    tar -xzf "node-v$NODE_VERSION-linux-x64.tar.gz" -C /usr/local --strip-components=1 && \
    rm -f "node-v$NODE_VERSION-linux-x64.tar.gz"

RUN npm install -g cnpm --registry=https://registry.npm.taobao.org && \
    cnpm i -g chromedriver geckodriver

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && ln -s /opt/google/chrome/chrome /usr/bin/chrome && sed -i 's#exec -a "$0" "$HERE/chrome" "$@"#exec -a "$0" "$HERE/chrome" "$@" "--no-sandbox"#g' /usr/bin/google-chrome
ENTRYPOINT ["/entrypoint.sh"]