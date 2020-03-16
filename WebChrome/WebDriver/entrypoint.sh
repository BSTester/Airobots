#!/bin/bash
# Java Environment Path
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH

export DISPLAY=':1'
export NODE_IN_DOCKER=1
export RESOLUTION=1920x1080

/startup.sh  &
if [ -e /etc/host ];then
    cat /etc/host >> /etc/hosts
fi
java -jar /opt/selenium-server-standalone.jar -role node -hub http://grid:4444/grid/register