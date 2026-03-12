# Base Image
FROM registry.cn-beijing.aliyuncs.com/opsany/python:3.12.5-slim-bullseye

# Crate Install PATH
RUN mkdir -p /opt/opsany/logs/opsany-mcp-server && mkdir /etc/supervisord.d

# Add Code File
ADD ./opsany-mcp-server /opt/opsany/opsany-mcp-server

# Install Python Env
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && sed -i 's/security.debian.org/mirrors.aliyun.com/g'  /etc/apt/sources.list \
    && echo "deb http://mirrors.aliyun.com/debian-security bullseye-security main contrib non-free" >> /etc/apt/sources.list \
    && apt-get update && apt-get -y install build-essential net-tools vim supervisor openssh-client \
    && apt-get clean \
    && pip --no-cache-dir install -r /opt/opsany/opsany-mcp-server/requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

#Supervisord Config
ADD supervisord.conf /etc/supervisord.conf
ADD mcp-supervisor.ini /etc/supervisord.d/mcp.ini

# Outside Port
EXPOSE 8020

#supervisord start
CMD ["supervisord", "-c", "/etc/supervisord.conf"]
