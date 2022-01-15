
FROM adoptopenjdk/openjdk14:jdk-14.0.2_12-debian

RUN apt update -y
RUN apt upgrade -y
RUN apt install -y unzip

COPY db-agent.zip db-agent.zip
RUN mkdir -p /opt/appd-dbagent
RUN unzip /db-agent.zip -d /opt/appd-dbagent

ENTRYPOINT java -Xmx3g -Ddbagent.name=${DB_AGENT_NAME:-north-west-blue} -jar /opt/appd-dbagent/db-agent.jar