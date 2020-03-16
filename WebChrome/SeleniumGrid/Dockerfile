FROM java

EXPOSE 4444

VOLUME /data
WORKDIR /data

RUN curl -o /opt/selenium-server-standalone.jar -L https://npm.taobao.org/mirrors/selenium/3.141/selenium-server-standalone-3.141.59.jar

CMD ["java", "-jar", "/opt/selenium-server-standalone.jar", "-role", "hub", "-browserTimeout", "60"]