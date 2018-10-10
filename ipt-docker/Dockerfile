FROM ubuntu:18.04
MAINTAINER Pieter Provoost <pieterprovoost@gmail.com>
EXPOSE 8080

VOLUME /usr/local/ipt/data

RUN apt-get update
RUN apt-get install -y --allow-unauthenticated wget default-jdk unzip

RUN wget -P /usr/local/ipt http://apache.belnet.be/tomcat/tomcat-8/v8.5.8/bin/apache-tomcat-8.5.8.tar.gz \
	&& tar -xvzf /usr/local/ipt/apache-tomcat-8.5.8.tar.gz -C /usr/local/ipt \
	&& wget -P /usr/local/ipt/apache-tomcat-8.5.8/webapps http://repository.gbif.org/content/groups/gbif/org/gbif/ipt/2.3.2/ipt-2.3.2.war \ 
	&& rm -r /usr/local/ipt/apache-tomcat-8.5.8/webapps/ROOT \
	&& unzip /usr/local/ipt/apache-tomcat-8.5.8/webapps/ipt-2.3.2.war -d /usr/local/ipt/apache-tomcat-8.5.8/webapps/ROOT \
	&& echo "/usr/local/ipt/data" > /usr/local/ipt/apache-tomcat-8.5.8/webapps/ROOT/WEB-INF/datadir.location

CMD /usr/local/ipt/apache-tomcat-8.5.8/bin/catalina.sh run
