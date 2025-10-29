#!/bin/bash
#******************************************
# Author:       Jason Zhao
# Email:        zhaoshundong@opsany.com
# Organization: OpsAny https://www.opsany.com/
# Description:  OpsAny Community Edition Update Script
#******************************************

# Data/Time Variables
CTIME=$(date "+%Y-%m-%d-%H-%M")

# Shell Envionment Variables
CDIR=$(pwd)
SHELL_NAME="opsany-ce-update.sh"
SHELL_LOG="${SHELL_NAME}.log"
ADMIN_PASSWORD=""

# Shell Log Record
shell_log(){
    # Show green
    LOG_INFO=$1
    echo -e "\033[32m---------------- $CTIME ${SHELL_NAME} : ${LOG_INFO} ----------------\033[0m"
    echo "$CTIME ${SHELL_NAME} : ${LOG_INFO}" >> ${SHELL_LOG}
}

shell_warning_log(){
    # Show yellow
    LOG_INFO=$1
    echo -e "\033[33m---------------- $CTIME ${SHELL_NAME} : ${LOG_INFO} ----------------\033[0m"
    echo "$CTIME ${SHELL_NAME} : ${LOG_INFO}" >> ${SHELL_LOG}
}

shell_error_log(){
    # Show red
    LOG_INFO=$1
    echo -e "\033[31m---------------- $CTIME ${SHELL_NAME} : ${LOG_INFO} ----------------\033[0m"
    echo "$CTIME ${SHELL_NAME} : ${LOG_INFO}" >> ${SHELL_LOG}
}

# Install Inspection
if [ ! -f ./install.config ];then
      shell_error_log "Please Change Directory to ${INSTALL_PATH}/install"
      exit
else
    grep '^[A-Z]' install.config > install.env
    source ./install.env && rm -f install.env
    if [ -z "$ADMIN_PASSWORD" ];then
        source ${INSTALL_PATH}/conf/.passwd_env
    fi
    mkdir -p ${INSTALL_PATH}/conf/opsany-paas/{paas,esb,login,appengine,websocket}
    # copy init script to websocket
    docker cp ../saas/ opsany-paas-websocket:/opt/opsany/
    docker cp ./init/ opsany-paas-websocket:/opt/opsany/

fi

# PaaS Service Update
paas_update(){
    #paas
    shell_log "======Update paas Service======"
    # PaaS Config
    UPDATE_VERSION=$1
    /bin/cp conf/opsany-paas/paas/paas.ini ${INSTALL_PATH}/conf/opsany-paas/paas/paas.ini
    /bin/cp conf/opsany-paas/paas/settings_production.py.paas ${INSTALL_PATH}/conf/opsany-paas/paas/settings_production.py.paas
    sed -i "s/PAAS_LOGIN_IP/${PAAS_LOGIN_IP}/g" ${INSTALL_PATH}/conf/opsany-paas/paas/settings_production.py.paas
    sed -i "s/PAAS_APPENGINE_IP/${PAAS_APPENGINE_IP}/g" ${INSTALL_PATH}/conf/opsany-paas/paas/settings_production.py.paas
    sed -i "s/DOMAIN_NAME/${DOMAIN_NAME}/g" ${INSTALL_PATH}/conf/opsany-paas/paas/settings_production.py.paas
    sed -i "s/LOCAL_IP/${LOCAL_IP}/g" ${INSTALL_PATH}/conf/opsany-paas/paas/settings_production.py.paas
    sed -i "s/MYSQL_SERVER_IP/${MYSQL_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-paas/paas/settings_production.py.paas
    sed -i "s/MYSQL_OPSANY_PASSWORD/${MYSQL_OPSANY_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-paas/paas/settings_production.py.paas
    sed -i "s/MYSQL_SERVER_PORT/${MYSQL_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-paas/paas/settings_production.py.paas

    docker stop opsany-paas-paas && docker rm opsany-paas-paas 
    docker pull ${PAAS_DOCKER_REG}/opsany-paas-paas:${UPDATE_VERSION}
    docker run -d --restart=always --name opsany-paas-paas \
    -p 8001:8001 -v ${INSTALL_PATH}/logs:/opt/opsany/logs \
    -v ${INSTALL_PATH}/conf/opsany-paas/paas/settings_production.py.paas:/opt/opsany/paas/paas/conf/settings_production.py \
    -v ${INSTALL_PATH}/conf/opsany-paas/paas/paas.ini:/etc/supervisord.d/paas.ini \
    -v /etc/localtime:/etc/localtime:ro \
    ${PAAS_DOCKER_REG}/opsany-paas-paas:${UPDATE_VERSION}
}

login_update(){
 #login
    shell_log "Start login Service"
    #Login Config
    UPDATE_VERSION=$1
    RBAC_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.rbac_secret_key)
    /bin/cp conf/opsany-paas/login/login.ini ${INSTALL_PATH}/conf/opsany-paas/login/login.ini
    /bin/cp conf/opsany-paas/login/settings_production.py.login ${INSTALL_PATH}/conf/opsany-paas/login/settings_production.py.login
    sed -i "s/RBAC_SECRET_KEY/${RBAC_SECRET_KEY}/g" ${INSTALL_PATH}/conf/opsany-paas/login/settings_production.py.login
    sed -i "s/DOMAIN_NAME/${DOMAIN_NAME}/g" ${INSTALL_PATH}/conf/opsany-paas/login/settings_production.py.login
    sed -i "s/LOCAL_IP/${LOCAL_IP}/g" ${INSTALL_PATH}/conf/opsany-paas/login/settings_production.py.login
    sed -i "s/MYSQL_SERVER_IP/${MYSQL_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-paas/login/settings_production.py.login
    sed -i "s/MYSQL_OPSANY_PASSWORD/${MYSQL_OPSANY_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-paas/login/settings_production.py.login
    sed -i "s/MYSQL_SERVER_PORT/${MYSQL_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-paas/login/settings_production.py.login

    docker stop opsany-paas-login && docker rm opsany-paas-login 
    docker pull ${PAAS_DOCKER_REG}/opsany-paas-login:${UPDATE_VERSION}
    docker run -d --restart=always --name opsany-paas-login \
    -p 8003:8003 -v ${INSTALL_PATH}/logs:/opt/opsany/logs \
    -v ${INSTALL_PATH}/conf/opsany-paas/login/settings_production.py.login:/opt/opsany/paas/login/conf/settings_production.py \
    -v ${INSTALL_PATH}/conf/opsany-paas/login/login.ini:/etc/supervisord.d/login.ini \
    -v /etc/localtime:/etc/localtime:ro \
    ${PAAS_DOCKER_REG}/opsany-paas-login:${UPDATE_VERSION}
}

esb_update(){
#esb
    shell_log "Start esb Service"

# ESB Components Update
    shell_log "======ESB Update======"
    /bin/cp -r ../paas-ce/paas/esb/components/generic/apis/* ${INSTALL_PATH}/esb/apis/
    #cmdb
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/cmdb/toolkit/configs.py
    sed -i "s#/t/cmdb#/o/cmdb#g" ${INSTALL_PATH}/esb/apis/cmdb/toolkit/tools.py
    #control
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/control/toolkit/configs.py
    sed -i "s#/t/control#/o/control#g" ${INSTALL_PATH}/esb/apis/control/toolkit/tools.py
    #rbac
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/rbac/toolkit/configs.py
    sed -i "s#/t/rbac#/o/rbac#g" ${INSTALL_PATH}/esb/apis/rbac/toolkit/configs.py
    #job
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/task/toolkit/configs.py
    sed -i "s#/t/job#/o/job#g" ${INSTALL_PATH}/esb/apis/task/toolkit/tools.py
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/job/toolkit/configs.py
    sed -i "s#/t/job#/o/job#g" ${INSTALL_PATH}/esb/apis/job/toolkit/tools.py
    #workbench
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/workbench/toolkit/configs.py
    sed -i "s#/t/workbench#/o/workbench#g" ${INSTALL_PATH}/esb/apis/workbench/toolkit/tools.py
    #monitor
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/monitor/toolkit/configs.py
    sed -i "s#/t/monitor#/o/monitor#g" ${INSTALL_PATH}/esb/apis/monitor/toolkit/tools.py
    #cmp
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/cmp/toolkit/configs.py
    sed -i "s#/t/cmp#/o/cmp#g" ${INSTALL_PATH}/esb/apis/cmp/toolkit/tools.py
    #devops
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/devops/toolkit/configs.py
    sed -i "s#/t/devops#/o/devops#g" ${INSTALL_PATH}/esb/apis/devops/toolkit/tools.py
    #pipeline
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/pipeline/toolkit/configs.py
    sed -i "s#/t/pipeline#/o/pipeline#g" ${INSTALL_PATH}/esb/apis/pipeline/toolkit/tools.py
    #deploy
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/deploy/toolkit/configs.py
    sed -i "s#/t/deploy#/o/deploy#g" ${INSTALL_PATH}/esb/apis/deploy/toolkit/tools.py
    #repo
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/repo/toolkit/configs.py
    sed -i "s#/t/repo#/o/repo#g" ${INSTALL_PATH}/esb/apis/repo/toolkit/tools.py
    #code
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/code/toolkit/configs.py
    sed -i "s#/t/code#/o/code#g" ${INSTALL_PATH}/esb/apis/code/toolkit/tools.py
    #bastion
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/bastion/toolkit/configs.py
    sed -i "s#/t/bastion#/o/bastion#g" ${INSTALL_PATH}/esb/apis/bastion/toolkit/configs.py
    # llmops
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/llmops/toolkit/configs.py
    sed -i "s#/t/llmops#/o/llmops#g" ${INSTALL_PATH}/esb/apis/llmops/toolkit/configs.py
    #prom
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/prom/toolkit/configs.py
    sed -i "s#/t/prom#/o/prom#g" ${INSTALL_PATH}/esb/apis/prom/toolkit/tools.py
    #auto
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/auto/toolkit/configs.py
    sed -i "s#/t/auto#/o/auto#g" ${INSTALL_PATH}/esb/apis/auto/toolkit/tools.py
    #dashboard
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/dashboard/toolkit/configs.py
    sed -i "s#/t/dashboard#/o/dashboard#g" ${INSTALL_PATH}/esb/apis/dashboard/toolkit/tools.py
    #event
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/event/toolkit/configs.py
    sed -i "s#/t/event#/o/event#g" ${INSTALL_PATH}/esb/apis/event/toolkit/tools.py
    #k8s
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/k8s/toolkit/configs.py
    sed -i "s#/t/k8s#/o/k8s#g" ${INSTALL_PATH}/esb/apis/k8s/toolkit/tools.py
    #kbase
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/kbase/toolkit/configs.py
    sed -i "s#/t/kbase#/o/kbase#g" ${INSTALL_PATH}/esb/apis/kbase/toolkit/tools.py
    #log
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/log/toolkit/configs.py
    sed -i "s#/t/log#/o/log#g" ${INSTALL_PATH}/esb/apis/log/toolkit/tools.py
    #apm
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/apm/toolkit/configs.py
    sed -i "s#/t/apm#/o/apm#g" ${INSTALL_PATH}/esb/apis/apm/toolkit/tools.py

    # update esb sql
    mysql -h "${MYSQL_SERVER_IP}" -P ${MYSQL_SERVER_PORT} -u root -p"${MYSQL_ROOT_PASSWORD}" opsany_paas < ./init/esb-init/esb_api_doc.sql
    mysql -h "${MYSQL_SERVER_IP}" -P ${MYSQL_SERVER_PORT} -u root -p"${MYSQL_ROOT_PASSWORD}" opsany_paas < ./init/esb-init/esb_channel.sql
    mysql -h "${MYSQL_SERVER_IP}" -P ${MYSQL_SERVER_PORT} -u root -p"${MYSQL_ROOT_PASSWORD}" opsany_paas < ./init/esb-init/esb_component_system.sql
    mysql -h "${MYSQL_SERVER_IP}" -P ${MYSQL_SERVER_PORT} -u root -p"${MYSQL_ROOT_PASSWORD}" opsany_paas < ./init/esb-init/esb_function_controller.sql

    # ESB Config
    UPDATE_VERSION=$1
    /bin/cp conf/opsany-paas/esb/esb.ini ${INSTALL_PATH}/conf/opsany-paas/esb/esb.ini
    /bin/cp conf/opsany-paas/esb/settings_production.py.esb ${INSTALL_PATH}/conf/opsany-paas/esb/settings_production.py.esb
    sed -i "s/PAAS_LOGIN_IP/${PAAS_LOGIN_IP}/g" ${INSTALL_PATH}/conf/opsany-paas/esb/settings_production.py.esb
    sed -i "s/PAAS_PAAS_IP/${PAAS_PAAS_IP}/g" ${INSTALL_PATH}/conf/opsany-paas/esb/settings_production.py.esb
    sed -i "s/REDIS_SERVER_IP/${REDIS_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-paas/esb/settings_production.py.esb
    sed -i "s/REDIS_SERVER_PASSWORD/${REDIS_SERVER_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-paas/esb/settings_production.py.esb
    sed -i "s/MYSQL_SERVER_IP/${MYSQL_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-paas/esb/settings_production.py.esb
    sed -i "s/MYSQL_OPSANY_PASSWORD/${MYSQL_OPSANY_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-paas/esb/settings_production.py.esb
    sed -i "s/MYSQL_SERVER_PORT/${MYSQL_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-paas/esb/settings_production.py.esb

    docker stop opsany-paas-esb && docker rm opsany-paas-esb 
    docker pull ${PAAS_DOCKER_REG}/opsany-paas-esb:${UPDATE_VERSION}
    docker run -d --restart=always --name opsany-paas-esb \
    -p 8002:8002 -v ${INSTALL_PATH}/logs:/opt/opsany/logs \
    -v ${INSTALL_PATH}/esb/apis:/opt/opsany/paas/esb/components/generic/apis \
    -v ${INSTALL_PATH}/conf/opsany-paas/esb/settings_production.py.esb:/opt/opsany/paas/esb/configs/default.py \
    -v ${INSTALL_PATH}/conf/opsany-paas/esb/esb.ini:/etc/supervisord.d/esb.ini \
    -v /etc/localtime:/etc/localtime:ro \
    ${PAAS_DOCKER_REG}/opsany-paas-esb:${UPDATE_VERSION}
}  

appengine_update(){
 #appengine
    # App Engine Config
    UPDATE_VERSION=$1
    /bin/cp conf/opsany-paas/appengine/appengine.ini ${INSTALL_PATH}/conf/opsany-paas/appengine/appengine.ini
    /bin/cp conf/opsany-paas/appengine/settings_production.py.appengine ${INSTALL_PATH}/conf/opsany-paas/appengine/settings_production.py.appengine
    sed -i "s/MYSQL_SERVER_IP/${MYSQL_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-paas/appengine/settings_production.py.appengine
    sed -i "s/MYSQL_OPSANY_PASSWORD/${MYSQL_OPSANY_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-paas/appengine/settings_production.py.appengine
    sed -i "s/MYSQL_SERVER_PORT/${MYSQL_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-paas/appengine/settings_production.py.appengine
    shell_log "Start appengine Service"

    docker stop opsany-paas-appengine && docker rm opsany-paas-appengine 
    docker pull ${PAAS_DOCKER_REG}/opsany-paas-appengine:${UPDATE_VERSION}
    docker run -d --restart=always --name opsany-paas-appengine \
    -p 8000:8000 -v ${INSTALL_PATH}/logs:/opt/opsany/logs \
    -v ${INSTALL_PATH}/conf/opsany-paas/appengine/settings_production.py.appengine:/opt/opsany/paas/appengine/controller/settings.py \
    -v ${INSTALL_PATH}/conf/opsany-paas/appengine/appengine.ini:/etc/supervisord.d/appengine.ini \
    -v /etc/localtime:/etc/localtime:ro \
    ${PAAS_DOCKER_REG}/opsany-paas-appengine:${UPDATE_VERSION}
}  

# Update Proxy
proxy_update(){
    shell_log "======Update Proxy======"
    UPDATE_VERSION=$1
    # Proxy config
    CONTROL_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.control_secret_key)
    /bin/cp conf/proxy/proxy.ini ${INSTALL_PATH}/conf/proxy/proxy.ini
    #/bin/cp conf/proxy/saltapi.ini ${INSTALL_PATH}/conf/proxy/saltapi.ini
    /bin/cp conf/proxy/saltmaster.ini ${INSTALL_PATH}/conf/proxy/saltmaster.ini
    /bin/cp conf/proxy/settings_production.py.proxy ${INSTALL_PATH}/conf/proxy/
    #/bin/cp conf/salt/master.d/api.conf ${INSTALL_PATH}/proxy-volume/etc/salt/master.d/
    #/bin/cp conf/salt/master.d/user.conf ${INSTALL_PATH}/proxy-volume/etc/salt/master.d/
    /bin/cp conf/salt/master ${INSTALL_PATH}/proxy-volume/etc/salt/
    /bin/cp conf/salt/minion ${INSTALL_PATH}/proxy-volume/etc/salt/
    sed -i "s/REDIS_SERVER_IP/${REDIS_SERVER_IP}/g" ${INSTALL_PATH}/conf/proxy/settings_production.py.proxy
    sed -i "s/REDIS_SERVER_PORT/${REDIS_SERVER_PORT}/g" ${INSTALL_PATH}/conf/proxy/settings_production.py.proxy
    sed -i "s/REDIS_SERVER_PASSWORD/${REDIS_SERVER_PASSWORD}/g" ${INSTALL_PATH}/conf/proxy/settings_production.py.proxy
    sed -i "s/MYSQL_SERVER_IP/${MYSQL_SERVER_IP}/g" ${INSTALL_PATH}/conf/proxy/settings_production.py.proxy
    sed -i "s/MYSQL_SERVER_PORT/${MYSQL_SERVER_PORT}/g" ${INSTALL_PATH}/conf/proxy/settings_production.py.proxy
    sed -i "s/MYSQL_OPSANY_PASSWORD/${MYSQL_OPSANY_PASSWORD}/g" ${INSTALL_PATH}/conf/proxy/settings_production.py.proxy
    sed -i "s/local-proxy.opsany.com/${PROXY_LOCAL_IP}/g" ${INSTALL_PATH}/conf/proxy/settings_production.py.proxy
    sed -i "s/public-proxy.opsany.com/${PROXY_PUBLIC_IP}/g" ${INSTALL_PATH}/conf/proxy/settings_production.py.proxy
    sed -i "s/LOCAL_IP/${PROXY_PUBLIC_IP} ${PROXY_LOCAL_IP}/g" ${INSTALL_PATH}/conf/proxy/nginx-conf.d/nginx_proxy.conf
    sed -i "s/DOMAIN_NAME/${PROXY_PUBLIC_IP} ${PROXY_LOCAL_IP}/g" ${INSTALL_PATH}/conf/proxy/nginx-conf.d/nginx_proxy.conf
    sed -i "s/RABBIT_SERVER_IP/${RABBIT_SERVER_IP}/g" ${INSTALL_PATH}/conf/proxy/settings_production.py.proxy
    sed -i "s/RABBITMQ_DEFAULT_USER/${RABBITMQ_DEFAULT_USER}/g" ${INSTALL_PATH}/conf/proxy/settings_production.py.proxy
    sed -i "s/RABBITMQ_DEFAULT_PASS/${RABBITMQ_DEFAULT_PASS}/g" ${INSTALL_PATH}/conf/proxy/settings_production.py.proxy
    sed -i "s/CONTROL_SECRET_KEY_PROXY/${CONTROL_SECRET_KEY}/g" ${INSTALL_PATH}/conf/proxy/settings_production.py.proxy
    cp ../saas/invscript_proxy.py ${INSTALL_PATH}/conf/proxy/
    sed -i "s/LOCALHOST/${MYSQL_SERVER_IP}/g" ${INSTALL_PATH}/conf/proxy/invscript_proxy.py
    sed -i "s/PROXY_PASSWORD/${MYSQL_OPSANY_PASSWORD}/g" ${INSTALL_PATH}/conf/proxy/invscript_proxy.py
    sed -i "s/CONTROL_SECRET_KEY/${CONTROL_SECRET_KEY}/g" ${INSTALL_PATH}/conf/proxy/invscript_proxy.py
    sed -i "s/MYSQL_SERVER_PORT/${MYSQL_SERVER_PORT}/g" ${INSTALL_PATH}/conf/proxy/invscript_proxy.py
    chmod +x ${INSTALL_PATH}/conf/proxy/invscript_proxy.py

    # Starter container
    docker stop opsany-paas-proxy && docker rm opsany-paas-proxy 
    docker pull ${PAAS_DOCKER_REG}/opsany-paas-proxy:${UPDATE_VERSION}
    mkdir -p ${INSTALL_PATH}/logs/proxy
    docker run --restart=always --name opsany-paas-proxy -d \
        -p 4505:4505 -p 4506:4506 -p 8010:8010 \
        -v ${INSTALL_PATH}/logs/proxy:/opt/opsany/logs/proxy \
        -v ${INSTALL_PATH}/proxy-volume/certs/:/etc/pki/tls/certs/ \
        -v ${INSTALL_PATH}/proxy-volume/etc/salt/:/etc/salt/ \
        -v ${INSTALL_PATH}/proxy-volume/cache/:/var/cache/salt/ \
        -v ${INSTALL_PATH}/proxy-volume/srv/salt:/srv/salt/ \
        -v ${INSTALL_PATH}/proxy-volume/srv/pillar:/srv/pillar/ \
        -v ${INSTALL_PATH}/proxy-volume/srv/playbook:/srv/playbook/ \
        -v ${INSTALL_PATH}/proxy-volume/pki:/opt/opsany/pki \
        -v ${INSTALL_PATH}/uploads:/opt/opsany/uploads \
        -v ${INSTALL_PATH}/conf/proxy/settings_production.py.proxy:/opt/opsany-proxy/config/prod.py \
        -v ${INSTALL_PATH}/conf/proxy/invscript_proxy.py:/opt/opsany-proxy/invscript_proxy.py \
        -v ${INSTALL_PATH}/conf/proxy/proxy.ini:/etc/supervisord.d/proxy.ini \
        -v ${INSTALL_PATH}/conf/proxy/saltmaster.ini:/etc/supervisord.d/saltmaster.ini \
        -v ${INSTALL_PATH}/prometheus-volume/conf/alertmanager.yml:/opt/opsany/alertmanager.yml \
        -v /etc/localtime:/etc/localtime:ro \
        ${PAAS_DOCKER_REG}/opsany-paas-proxy:${UPDATE_VERSION}

    # OpsAny Database Init
    docker exec -e OPS_ANY_ENV=production \
        opsany-paas-proxy /bin/sh -c "/usr/local/bin/python3 /opt/opsany-proxy/manage.py migrate >> ${SHELL_LOG}"
}
saas_llmops_update(){
    shell_log "======Update llmops======"

    #llmops Configure
    UPDATE_VERSION=$1
    LLMOPS_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.llmops_secret_key)
    /bin/cp conf/opsany-saas/llmops/* ${INSTALL_PATH}/conf/opsany-saas/llmops/
    sed -i "s/DOMAIN_NAME/${DOMAIN_NAME}/g" ${INSTALL_PATH}/conf/opsany-saas/llmops/llmops-init.py
    sed -i "s/LLMOPS_SECRET_KEY/${LLMOPS_SECRET_KEY}/g" ${INSTALL_PATH}/conf/opsany-saas/llmops/llmops-init.py
    sed -i "s/MYSQL_SERVER_IP/${MYSQL_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/llmops/llmops-prod.py
    sed -i "s/MYSQL_SERVER_PORT/${MYSQL_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/llmops/llmops-prod.py
    sed -i "s/MYSQL_OPSANY_LLMOPS_PASSWORD/${MYSQL_OPSANY_LLMOPS_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/llmops/llmops-prod.py
    sed -i "s/MONGO_SERVER_IP/${MONGO_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/llmops/llmops-prod.py
    sed -i "s/MONGO_SERVER_PORT/${MONGO_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/llmops/llmops-prod.py
    sed -i "s/MONGO_LLMOPS_PASSWORD/${MONGO_LLMOPS_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/llmops/llmops-prod.py
    sed -i "s/REDIS_SERVER_IP/${REDIS_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/llmops/llmops-prod.py
    sed -i "s/REDIS_SERVER_PORT/${REDIS_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/llmops/llmops-prod.py
    sed -i "s/REDIS_SERVER_USER/${REDIS_SERVER_USER}/g" ${INSTALL_PATH}/conf/opsany-saas/llmops/llmops-prod.py
    sed -i "s/REDIS_SERVER_PASSWORD/${REDIS_SERVER_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/llmops/llmops-prod.py

    # llmops
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/llmops/toolkit/configs.py
    sed -i "s#/t/llmops#/o/llmops#g" ${INSTALL_PATH}/esb/apis/llmops/toolkit/configs.py

    # Starter container
    docker pull ${PAAS_DOCKER_REG}/opsany-saas-ce-llmops:${UPDATE_VERSION}
    docker stop opsany-saas-ce-llmops && docker rm opsany-saas-ce-llmops
    docker run -d --restart=always --name opsany-saas-ce-llmops \
       -p 7000:80 \
       -v ${INSTALL_PATH}/conf/opsany-saas/llmops/llmops-supervisor.ini:/etc/supervisord.d/llmops.ini \
       -v ${INSTALL_PATH}/conf/opsany-saas/llmops/llmops-uwsgi.ini:/opt/opsany/uwsgi/llmops.ini \
       -v ${INSTALL_PATH}/conf/opsany-saas/llmops/llmops-init.py:/opt/opsany/llmops/config/__init__.py \
       -v ${INSTALL_PATH}/conf/opsany-saas/llmops/llmops-prod.py:/opt/opsany/llmops/config/prod.py \
       -v ${INSTALL_PATH}/conf/opsany-saas/llmops/llmops-nginx.conf:/etc/nginx/http.d/default.conf \
       -v ${INSTALL_PATH}/conf/opsany-saas/llmops/llmops-nginx-main.conf:/etc/nginx/nginx.conf \
       -v ${INSTALL_PATH}/logs/llmops:/opt/opsany/logs/llmops \
       -v ${INSTALL_PATH}/uploads:/opt/opsany/uploads \
       -v /etc/localtime:/etc/localtime:ro \
       ${PAAS_DOCKER_REG}/opsany-saas-ce-llmops:${UPDATE_VERSION}
    
    # Django migrate
    docker exec -e BK_ENV="production" opsany-saas-ce-llmops /bin/sh -c \
    "python /opt/opsany/llmops/manage.py migrate --noinput >> ${SHELL_LOG} && python /opt/opsany/llmops/manage.py createcachetable django_cache > /dev/null"
    update_saas_version llmops 大模型开发平台 ${LLMOPS_SECRET_KEY}
}
websocket_update(){
# Websocket
    UPDATE_VERSION=$1
    BASTION_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.bastion_secret_key)
    /bin/cp conf/opsany-paas/websocket/websocket.ini ${INSTALL_PATH}/conf/opsany-paas/websocket/websocket.ini
    /bin/cp conf/opsany-paas/websocket/settings_production.py.websocket ${INSTALL_PATH}/conf/opsany-paas/websocket/settings_production.py.websocket
    /bin/cp conf/opsany-paas/websocket/settings_production.py.websocket.init ${INSTALL_PATH}/conf/opsany-paas/websocket/settings_production.py.websocket.init
    sed -i "s/BASTION_SECRET_KEY/${BASTION_SECRET_KEY}/g" ${INSTALL_PATH}/conf/opsany-paas/websocket/settings_production.py.websocket.init
    sed -i "s/WEBSOCKET_GUACD_HOST/${WEBSOCKET_GUACD_HOST}/g" ${INSTALL_PATH}/conf/opsany-paas/websocket/settings_production.py.websocket
    sed -i "s/REDIS_SERVER_IP/${REDIS_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-paas/websocket/settings_production.py.websocket
    sed -i "s/REDIS_SERVER_USER/${REDIS_SERVER_USER}/g" ${INSTALL_PATH}/conf/opsany-paas/websocket/settings_production.py.websocket
    sed -i "s/REDIS_SERVER_PORT/${REDIS_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-paas/websocket/settings_production.py.websocket
    sed -i "s/REDIS_SERVER_PASSWORD/${REDIS_SERVER_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-paas/websocket/settings_production.py.websocket
    sed -i "s/MYSQL_SERVER_IP/${MYSQL_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-paas/websocket/settings_production.py.websocket
    sed -i "s/MYSQL_SERVER_PORT/${MYSQL_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-paas/websocket/settings_production.py.websocket
    sed -i "s/MYSQL_OPSANY_PASSWORD/${MYSQL_OPSANY_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-paas/websocket/settings_production.py.websocket
    sed -i "s/PAAS_PAAS_IP/${PAAS_PAAS_IP}/g" ${INSTALL_PATH}/conf/opsany-paas/websocket/settings_production.py.websocket.init
    docker stop opsany-paas-websocket && docker rm opsany-paas-websocket
    docker pull ${PAAS_DOCKER_REG}/opsany-paas-websocket:${UPDATE_VERSION}
    docker run -d --restart=always --name opsany-paas-websocket \
    -p 8004:8004 -v ${INSTALL_PATH}/logs:/opt/opsany/logs \
    -v ${INSTALL_PATH}/uploads:/opt/opsany/uploads \
    -v ${INSTALL_PATH}/conf/opsany-paas/websocket/settings_production.py.websocket:/opt/opsany/websocket/config/prod.py \
    -v ${INSTALL_PATH}/conf/opsany-paas/websocket/settings_production.py.websocket.init:/opt/opsany/websocket/config/__init__.py \
    -v ${INSTALL_PATH}/conf/opsany-paas/websocket/websocket.ini:/etc/supervisord.d/websocket.ini \
    -v /usr/share/zoneinfo:/usr/share/zoneinfo \
    -v /etc/localtime:/etc/localtime:ro \
    ${PAAS_DOCKER_REG}/opsany-paas-websocket:${UPDATE_VERSION}
    docker cp ../saas/ opsany-paas-websocket:/opt/opsany/
    docker cp ./init/ opsany-paas-websocket:/opt/opsany/
}

saas_rbac_update(){
    shell_log "======Update RBAC======"
    # Modify configuration
    UPDATE_VERSION=$1
    RBAC_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.rbac_secret_key)
    /bin/cp conf/opsany-saas/rbac/* ${INSTALL_PATH}/conf/opsany-saas/rbac/
    sed -i "s/DOMAIN_NAME/${DOMAIN_NAME}/g" ${INSTALL_PATH}/conf/opsany-saas/rbac/rbac-init.py
    sed -i "s/RBAC_SECRET_KEY/${RBAC_SECRET_KEY}/g" ${INSTALL_PATH}/conf/opsany-saas/rbac/rbac-init.py
    sed -i "s/MYSQL_SERVER_IP/${MYSQL_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/rbac/rbac-prod.py
    sed -i "s/MYSQL_SERVER_PORT/${MYSQL_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/rbac/rbac-prod.py
    sed -i "s/MYSQL_OPSANY_RBAC_PASSWORD/${MYSQL_OPSANY_RBAC_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/rbac/rbac-prod.py
    sed -i "s/REDIS_SERVER_IP/${REDIS_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/rbac/rbac-prod.py
    sed -i "s/REDIS_SERVER_PORT/${REDIS_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/rbac/rbac-prod.py
    sed -i "s/REDIS_SERVER_USER/${REDIS_SERVER_USER}/g" ${INSTALL_PATH}/conf/opsany-saas/rbac/rbac-prod.py
    sed -i "s/REDIS_SERVER_PASSWORD/${REDIS_SERVER_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/rbac/rbac-prod.py

    # Starter container
    docker stop opsany-saas-ce-rbac && docker rm opsany-saas-ce-rbac
    docker pull ${PAAS_DOCKER_REG}/opsany-saas-ce-rbac:${UPDATE_VERSION}
    docker run -d --restart=always --name opsany-saas-ce-rbac \
       -p 7001:80 \
       -v ${INSTALL_PATH}/conf/opsany-saas/rbac/rbac-supervisor.ini:/etc/supervisord.d/rbac.ini \
       -v ${INSTALL_PATH}/conf/opsany-saas/rbac/rbac-uwsgi.ini:/opt/opsany/uwsgi/rbac.ini \
       -v ${INSTALL_PATH}/conf/opsany-saas/rbac/rbac-init.py:/opt/opsany/rbac/config/__init__.py \
       -v ${INSTALL_PATH}/conf/opsany-saas/rbac/rbac-prod.py:/opt/opsany/rbac/config/prod.py \
       -v ${INSTALL_PATH}/conf/opsany-saas/rbac/rbac-nginx.conf:/etc/nginx/http.d/default.conf \
       -v ${INSTALL_PATH}/conf/opsany-saas/rbac/rbac-nginx-main.conf:/etc/nginx/nginx.conf \
       -v ${INSTALL_PATH}/logs/rbac:/opt/opsany/logs/rbac \
       -v ${INSTALL_PATH}/uploads:/opt/opsany/uploads \
       -v /etc/localtime:/etc/localtime:ro \
       ${PAAS_DOCKER_REG}/opsany-saas-ce-rbac:${UPDATE_VERSION}
    
    # Django migrate
    docker exec -e BK_ENV="production" opsany-saas-ce-rbac /bin/sh -c \
    "python /opt/opsany/rbac/manage.py migrate --noinput >> ${SHELL_LOG} && python /opt/opsany/rbac/manage.py createcachetable django_cache > /dev/null"
    update_saas_version rbac 统一权限 ${RBAC_SECRET_KEY}
}

saas_workbench_update(){
    shell_log "======Update workbench======"
    # Modify configuration
    UPDATE_VERSION=$1
    WORKBENCH_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.workbench_secret_key)
    /bin/cp conf/opsany-saas/workbench/* ${INSTALL_PATH}/conf/opsany-saas/workbench/
    sed -i "s/DOMAIN_NAME/${DOMAIN_NAME}/g" ${INSTALL_PATH}/conf/opsany-saas/workbench/workbench-init.py
    sed -i "s/WORKBENCH_SECRET_KEY/${WORKBENCH_SECRET_KEY}/g" ${INSTALL_PATH}/conf/opsany-saas/workbench/workbench-init.py
    sed -i "s/MYSQL_SERVER_IP/${MYSQL_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/workbench/workbench-prod.py
    sed -i "s/MYSQL_SERVER_PORT/${MYSQL_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/workbench/workbench-prod.py
    sed -i "s/MYSQL_OPSANY_WORKBENCH_PASSWORD/${MYSQL_OPSANY_WORKBENCH_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/workbench/workbench-prod.py
    sed -i "s/MONGO_SERVER_IP/${MONGO_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/workbench/workbench-prod.py
    sed -i "s/MONGO_SERVER_PORT/${MONGO_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/workbench/workbench-prod.py
    sed -i "s/MONGO_WORKBENCH_PASSWORD/${MONGO_WORKBENCH_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/workbench/workbench-prod.py
    sed -i "s/REDIS_SERVER_IP/${REDIS_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/workbench/workbench-prod.py
    sed -i "s/REDIS_SERVER_PORT/${REDIS_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/workbench/workbench-prod.py
    sed -i "s/REDIS_SERVER_USER/${REDIS_SERVER_USER}/g" ${INSTALL_PATH}/conf/opsany-saas/workbench/workbench-prod.py
    sed -i "s/REDIS_SERVER_PASSWORD/${REDIS_SERVER_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/workbench/workbench-prod.py

    #workbench
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/workbench/toolkit/configs.py
    sed -i "s#/t/workbench#/o/workbench#g" ${INSTALL_PATH}/esb/apis/workbench/toolkit/tools.py

    # Starter container
    docker pull ${PAAS_DOCKER_REG}/opsany-saas-ce-workbench:${UPDATE_VERSION}
    docker stop opsany-saas-ce-workbench && docker rm opsany-saas-ce-workbench
    docker run -d --restart=always --name opsany-saas-ce-workbench \
       -p 7002:80 \
       -v ${INSTALL_PATH}/conf/opsany-saas/workbench/workbench-supervisor.ini:/etc/supervisord.d/workbench.ini \
       -v ${INSTALL_PATH}/conf/opsany-saas/workbench/workbench-uwsgi.ini:/opt/opsany/uwsgi/workbench.ini \
       -v ${INSTALL_PATH}/conf/opsany-saas/workbench/workbench-init.py:/opt/opsany/workbench/config/__init__.py \
       -v ${INSTALL_PATH}/conf/opsany-saas/workbench/workbench-prod.py:/opt/opsany/workbench/config/prod.py \
       -v ${INSTALL_PATH}/conf/opsany-saas/workbench/workbench-nginx.conf:/etc/nginx/http.d/default.conf \
       -v ${INSTALL_PATH}/conf/opsany-saas/workbench/workbench-nginx-main.conf:/etc/nginx/nginx.conf \
       -v ${INSTALL_PATH}/logs/workbench:/opt/opsany/logs/workbench \
       -v ${INSTALL_PATH}/uploads:/opt/opsany/uploads \
       -v /etc/localtime:/etc/localtime:ro \
       ${PAAS_DOCKER_REG}/opsany-saas-ce-workbench:${UPDATE_VERSION}
    # Django migrate
    docker exec -e BK_ENV="production" opsany-saas-ce-workbench /bin/sh -c \
    "python /opt/opsany/workbench/manage.py migrate --noinput >> ${SHELL_LOG} >> ${SHELL_LOG} && python /opt/opsany/workbench/manage.py createcachetable django_cache > /dev/null"
    update_saas_version workbench 工作台 ${WORKBENCH_SECRET_KEY}
}

saas_cmdb_update(){
    shell_log "======Update cmdb======"
    # Modify configuration
    UPDATE_VERSION=$1
    CMDB_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.cmdb_secret_key)
    /bin/cp conf/opsany-saas/cmdb/* ${INSTALL_PATH}/conf/opsany-saas/cmdb/
    sed -i "s/DOMAIN_NAME/${DOMAIN_NAME}/g" ${INSTALL_PATH}/conf/opsany-saas/cmdb/cmdb-init.py
    sed -i "s/CMDB_SECRET_KEY/${CMDB_SECRET_KEY}/g" ${INSTALL_PATH}/conf/opsany-saas/cmdb/cmdb-init.py
    sed -i "s/MYSQL_SERVER_IP/${MYSQL_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/cmdb/cmdb-prod.py
    sed -i "s/MYSQL_SERVER_PORT/${MYSQL_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/cmdb/cmdb-prod.py
    sed -i "s/MYSQL_OPSANY_CMDB_PASSWORD/${MYSQL_OPSANY_CMDB_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/cmdb/cmdb-prod.py
    sed -i "s/MONGO_SERVER_IP/${MONGO_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/cmdb/cmdb-prod.py
    sed -i "s/MONGO_SERVER_PORT/${MONGO_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/cmdb/cmdb-prod.py
    sed -i "s/MONGO_CMDB_PASSWORD/${MONGO_CMDB_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/cmdb/cmdb-prod.py
    sed -i "s/REDIS_SERVER_IP/${REDIS_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/cmdb/cmdb-prod.py
    sed -i "s/REDIS_SERVER_PORT/${REDIS_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/cmdb/cmdb-prod.py
    sed -i "s/REDIS_SERVER_USER/${REDIS_SERVER_USER}/g" ${INSTALL_PATH}/conf/opsany-saas/cmdb/cmdb-prod.py
    sed -i "s/REDIS_SERVER_PASSWORD/${REDIS_SERVER_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/cmdb/cmdb-prod.py
    
    
    #cmdb
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/cmdb/toolkit/configs.py
    sed -i "s#/t/cmdb#/o/cmdb#g" ${INSTALL_PATH}/esb/apis/cmdb/toolkit/tools.py

    # Starter container
    docker pull ${PAAS_DOCKER_REG}/opsany-saas-ce-cmdb:${UPDATE_VERSION}
    docker stop opsany-saas-ce-cmdb && docker rm opsany-saas-ce-cmdb
    docker run -d --restart=always --name opsany-saas-ce-cmdb \
       -p 7003:80 \
       -v ${INSTALL_PATH}/conf/opsany-saas/cmdb/cmdb-supervisor.ini:/etc/supervisord.d/cmdb.ini \
       -v ${INSTALL_PATH}/conf/opsany-saas/cmdb/cmdb-uwsgi.ini:/opt/opsany/uwsgi/cmdb.ini \
       -v ${INSTALL_PATH}/conf/opsany-saas/cmdb/cmdb-init.py:/opt/opsany/cmdb/config/__init__.py \
       -v ${INSTALL_PATH}/conf/opsany-saas/cmdb/cmdb-prod.py:/opt/opsany/cmdb/config/prod.py \
       -v ${INSTALL_PATH}/conf/opsany-saas/cmdb/cmdb-nginx.conf:/etc/nginx/http.d/default.conf \
       -v ${INSTALL_PATH}/conf/opsany-saas/cmdb/cmdb-nginx-main.conf:/etc/nginx/nginx.conf \
       -v ${INSTALL_PATH}/logs/cmdb:/opt/opsany/logs/cmdb \
       -v ${INSTALL_PATH}/uploads:/opt/opsany/uploads \
       -v /etc/localtime:/etc/localtime:ro \
       ${PAAS_DOCKER_REG}/opsany-saas-ce-cmdb:${UPDATE_VERSION}
    
    # Django migrate
    docker exec -e BK_ENV="production" opsany-saas-ce-cmdb /bin/sh -c \
    "python /opt/opsany/cmdb/manage.py migrate --noinput >> ${SHELL_LOG} && python /opt/opsany/cmdb/manage.py createcachetable django_cache > /dev/null"
    update_saas_version cmdb 资源平台 ${CMDB_SECRET_KEY}
}

saas_control_update(){
    shell_log "======Update control======"
    # Modify configuration
    UPDATE_VERSION=$1
    CONTROL_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.control_secret_key)
    /bin/cp conf/opsany-saas/control/* ${INSTALL_PATH}/conf/opsany-saas/control/
    sed -i "s/DOMAIN_NAME/${DOMAIN_NAME}/g" ${INSTALL_PATH}/conf/opsany-saas/control/control-init.py
    sed -i "s/CONTROL_SECRET_KEY/${CONTROL_SECRET_KEY}/g" ${INSTALL_PATH}/conf/opsany-saas/control/control-init.py
    sed -i "s/MYSQL_SERVER_IP/${MYSQL_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/control/control-prod.py
    sed -i "s/MYSQL_SERVER_PORT/${MYSQL_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/control/control-prod.py
    sed -i "s/MYSQL_OPSANY_CONTROL_PASSWORD/${MYSQL_OPSANY_CONTROL_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/control/control-prod.py
    sed -i "s/REDIS_SERVER_IP/${REDIS_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/control/control-prod.py
    sed -i "s/REDIS_SERVER_PORT/${REDIS_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/control/control-prod.py
    sed -i "s/REDIS_SERVER_USER/${REDIS_SERVER_USER}/g" ${INSTALL_PATH}/conf/opsany-saas/control/control-prod.py
    sed -i "s/REDIS_SERVER_PASSWORD/${REDIS_SERVER_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/control/control-prod.py

    #control
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/control/toolkit/configs.py
    sed -i "s#/t/control#/o/control#g" ${INSTALL_PATH}/esb/apis/control/toolkit/tools.py

    # Starter container
    docker pull ${PAAS_DOCKER_REG}/opsany-saas-ce-control:${UPDATE_VERSION}
    docker stop opsany-saas-ce-control && docker rm opsany-saas-ce-control
    docker run -d --restart=always --name opsany-saas-ce-control \
       -p 7004:80 \
       -v ${INSTALL_PATH}/conf/opsany-saas/control/control-supervisor.ini:/etc/supervisord.d/control.ini \
       -v ${INSTALL_PATH}/conf/opsany-saas/control/control-uwsgi.ini:/opt/opsany/uwsgi/control.ini \
       -v ${INSTALL_PATH}/conf/opsany-saas/control/control-init.py:/opt/opsany/control/config/__init__.py \
       -v ${INSTALL_PATH}/conf/opsany-saas/control/control-prod.py:/opt/opsany/control/config/prod.py \
       -v ${INSTALL_PATH}/conf/opsany-saas/control/control-nginx.conf:/etc/nginx/http.d/default.conf \
       -v ${INSTALL_PATH}/conf/opsany-saas/control/control-nginx-main.conf:/etc/nginx/nginx.conf \
       -v ${INSTALL_PATH}/logs:/opt/opsany/logs \
       -v ${INSTALL_PATH}/uploads:/opt/opsany/uploads \
       -v /etc/localtime:/etc/localtime:ro \
       ${PAAS_DOCKER_REG}/opsany-saas-ce-control:${UPDATE_VERSION}
    
    # Django migrate
    docker exec -e BK_ENV="production" opsany-saas-ce-control /bin/sh -c \
    "python /opt/opsany/control/manage.py migrate --noinput >> ${SHELL_LOG} && python /opt/opsany/control/manage.py createcachetable django_cache > /dev/null"
    update_saas_version control 管控平台 ${CONTROL_SECRET_KEY}
}

saas_job_update(){
    shell_log "======Update job======"
    # Modify configuration
    UPDATE_VERSION=$1
    JOB_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.job_secret_key)
    /bin/cp conf/opsany-saas/job/* ${INSTALL_PATH}/conf/opsany-saas/job/
    sed -i "s/DOMAIN_NAME/${DOMAIN_NAME}/g" ${INSTALL_PATH}/conf/opsany-saas/job/job-init.py
    sed -i "s/JOB_SECRET_KEY/${JOB_SECRET_KEY}/g" ${INSTALL_PATH}/conf/opsany-saas/job/job-init.py
    sed -i "s/MYSQL_SERVER_IP/${MYSQL_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/job/job-prod.py
    sed -i "s/MYSQL_SERVER_PORT/${MYSQL_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/job/job-prod.py
    sed -i "s/MYSQL_OPSANY_JOB_PASSWORD/${MYSQL_OPSANY_JOB_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/job/job-prod.py
    sed -i "s/MONGO_SERVER_IP/${MONGO_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/job/job-prod.py
    sed -i "s/MONGO_SERVER_PORT/${MONGO_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/job/job-prod.py
    sed -i "s/MONGO_JOB_PASSWORD/${MONGO_JOB_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/job/job-prod.py
    sed -i "s/REDIS_SERVER_IP/${REDIS_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/job/job-prod.py
    sed -i "s/REDIS_SERVER_PORT/${REDIS_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/job/job-prod.py
    sed -i "s/REDIS_SERVER_USER/${REDIS_SERVER_USER}/g" ${INSTALL_PATH}/conf/opsany-saas/job/job-prod.py
    sed -i "s/REDIS_SERVER_PASSWORD/${REDIS_SERVER_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/job/job-prod.py
    
    #job
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/task/toolkit/configs.py
    sed -i "s#/t/job#/o/job#g" ${INSTALL_PATH}/esb/apis/task/toolkit/tools.py
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" ${INSTALL_PATH}/esb/apis/job/toolkit/configs.py
    sed -i "s#/t/job#/o/job#g" ${INSTALL_PATH}/esb/apis/job/toolkit/tools.py

    # Starter container
    docker pull ${PAAS_DOCKER_REG}/opsany-saas-ce-job:${UPDATE_VERSION}
    docker stop opsany-saas-ce-job && docker rm opsany-saas-ce-job
    docker run -d --restart=always --name opsany-saas-ce-job \
       -p 7005:80 \
       -v ${INSTALL_PATH}/conf/opsany-saas/job/job-supervisor.ini:/etc/supervisord.d/job.ini \
       -v ${INSTALL_PATH}/conf/opsany-saas/job/job-uwsgi.ini:/opt/opsany/uwsgi/job.ini \
       -v ${INSTALL_PATH}/conf/opsany-saas/job/job-init.py:/opt/opsany/job/config/__init__.py \
       -v ${INSTALL_PATH}/conf/opsany-saas/job/job-prod.py:/opt/opsany/job/config/prod.py \
       -v ${INSTALL_PATH}/conf/opsany-saas/job/job-nginx.conf:/etc/nginx/http.d/default.conf \
       -v ${INSTALL_PATH}/conf/opsany-saas/job/job-nginx-main.conf:/etc/nginx/nginx.conf \
       -v ${INSTALL_PATH}/logs/job:/opt/opsany/logs/job \
       -v ${INSTALL_PATH}/uploads:/opt/opsany/uploads \
       -v /etc/localtime:/etc/localtime:ro \
       ${PAAS_DOCKER_REG}/opsany-saas-ce-job:${UPDATE_VERSION}
    
    # Django migrate
    docker exec -e BK_ENV="production" opsany-saas-ce-job /bin/sh -c \
    "python /opt/opsany/job/manage.py migrate --noinput >> ${SHELL_LOG} && python /opt/opsany/job/manage.py createcachetable django_cache > /dev/null"
    update_saas_version job 作业平台 ${JOB_SECRET_KEY}
}

saas_monitor_update(){
    shell_log "======Update monitor======"

    # Modify configuration
    UPDATE_VERSION=$1
    MONITOR_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.monitor_secret_key)
    /bin/cp conf/opsany-saas/monitor/* ${INSTALL_PATH}/conf/opsany-saas/monitor/
    sed -i "s/DOMAIN_NAME/${DOMAIN_NAME}/g" ${INSTALL_PATH}/conf/opsany-saas/monitor/monitor-init.py
    sed -i "s/MONITOR_SECRET_KEY/${MONITOR_SECRET_KEY}/g" ${INSTALL_PATH}/conf/opsany-saas/monitor/monitor-init.py
    sed -i "s/MYSQL_SERVER_IP/${MYSQL_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/monitor/monitor-prod.py
    sed -i "s/MYSQL_SERVER_PORT/${MYSQL_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/monitor/monitor-prod.py
    sed -i "s/MYSQL_OPSANY_MONITOR_PASSWORD/${MYSQL_OPSANY_MONITOR_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/monitor/monitor-prod.py
    sed -i "s/MONGO_SERVER_IP/${MONGO_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/monitor/monitor-prod.py
    sed -i "s/MONGO_SERVER_PORT/${MONGO_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/monitor/monitor-prod.py
    sed -i "s/MONGO_MONITOR_PASSWORD/${MONGO_MONITOR_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/monitor/monitor-prod.py
    sed -i "s/REDIS_SERVER_IP/${REDIS_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/monitor/monitor-prod.py
    sed -i "s/REDIS_SERVER_PORT/${REDIS_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/monitor/monitor-prod.py
    sed -i "s/REDIS_SERVER_USER/${REDIS_SERVER_USER}/g" ${INSTALL_PATH}/conf/opsany-saas/monitor/monitor-prod.py
    sed -i "s/REDIS_SERVER_PASSWORD/${REDIS_SERVER_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/monitor/monitor-prod.py
    
    # Starter container
    docker pull ${PAAS_DOCKER_REG}/opsany-saas-ce-monitor:${UPDATE_VERSION}
    docker stop opsany-saas-ce-monitor && docker rm opsany-saas-ce-monitor
    docker run -d --restart=always --name opsany-saas-ce-monitor \
       -p 7006:80 \
       -v ${INSTALL_PATH}/conf/opsany-saas/monitor/monitor-supervisor.ini:/etc/supervisord.d/monitor.ini \
       -v ${INSTALL_PATH}/conf/opsany-saas/monitor/monitor-uwsgi.ini:/opt/opsany/uwsgi/monitor.ini \
       -v ${INSTALL_PATH}/conf/opsany-saas/monitor/monitor-init.py:/opt/opsany/monitor/config/__init__.py \
       -v ${INSTALL_PATH}/conf/opsany-saas/monitor/monitor-prod.py:/opt/opsany/monitor/config/prod.py \
       -v ${INSTALL_PATH}/conf/opsany-saas/monitor/monitor-nginx.conf:/etc/nginx/http.d/default.conf \
       -v ${INSTALL_PATH}/conf/opsany-saas/monitor/monitor-nginx-main.conf:/etc/nginx/nginx.conf \
       -v ${INSTALL_PATH}/logs/monitor:/opt/opsany/logs/monitor \
       -v ${INSTALL_PATH}/uploads:/opt/opsany/uploads \
       -v /etc/localtime:/etc/localtime:ro \
       ${PAAS_DOCKER_REG}/opsany-saas-ce-monitor:${UPDATE_VERSION}
    
    # Django migrate
    docker exec -e BK_ENV="production" opsany-saas-ce-monitor /bin/sh -c \
    "python /opt/opsany/monitor/manage.py migrate --noinput >> ${SHELL_LOG} && python /opt/opsany/monitor/manage.py createcachetable django_cache > /dev/null"
    update_saas_version monitor 基础监控 ${MONITOR_SECRET_KEY}

    shell_log "======Update Dashboard Initialize======"
    # Init Script Job
    docker exec opsany-paas-websocket /bin/sh -c "cd /opt/opsany/init/ && python3 init_dashboard.py --grafana_url https://${DOMAIN_NAME}/grafana/ --grafana_username admin --grafana_password $GRAFANA_ADMIN_PASSWORD"

}

saas_cmp_update(){
    shell_log "======Update cmp======"

    #CMP Configure
    UPDATE_VERSION=$1
    CMP_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.cmp_secret_key)
    /bin/cp conf/opsany-saas/cmp/* ${INSTALL_PATH}/conf/opsany-saas/cmp/
    sed -i "s/DOMAIN_NAME/${DOMAIN_NAME}/g" ${INSTALL_PATH}/conf/opsany-saas/cmp/cmp-init.py
    sed -i "s/CMP_SECRET_KEY/${CMP_SECRET_KEY}/g" ${INSTALL_PATH}/conf/opsany-saas/cmp/cmp-init.py
    sed -i "s/MYSQL_SERVER_IP/${MYSQL_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/cmp/cmp-prod.py
    sed -i "s/MYSQL_SERVER_PORT/${MYSQL_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/cmp/cmp-prod.py
    sed -i "s/MYSQL_OPSANY_CMP_PASSWORD/${MYSQL_OPSANY_CMP_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/cmp/cmp-prod.py
    sed -i "s/MONGO_SERVER_IP/${MONGO_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/cmp/cmp-prod.py
    sed -i "s/MONGO_SERVER_PORT/${MONGO_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/cmp/cmp-prod.py
    sed -i "s/MONGO_CMP_PASSWORD/${MONGO_CMP_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/cmp/cmp-prod.py
    sed -i "s/REDIS_SERVER_IP/${REDIS_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/cmp/cmp-prod.py
    sed -i "s/REDIS_SERVER_PORT/${REDIS_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/cmp/cmp-prod.py
    sed -i "s/REDIS_SERVER_USER/${REDIS_SERVER_USER}/g" ${INSTALL_PATH}/conf/opsany-saas/cmp/cmp-prod.py
    sed -i "s/REDIS_SERVER_PASSWORD/${REDIS_SERVER_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/cmp/cmp-prod.py
    
    # Starter container
    docker pull ${PAAS_DOCKER_REG}/opsany-saas-ce-cmp:${UPDATE_VERSION}
    docker stop opsany-saas-ce-cmp && docker rm opsany-saas-ce-cmp
    docker run -d --restart=always --name opsany-saas-ce-cmp \
       -p 7007:80 \
       -v ${INSTALL_PATH}/conf/opsany-saas/cmp/cmp-supervisor.ini:/etc/supervisord.d/cmp.ini \
       -v ${INSTALL_PATH}/conf/opsany-saas/cmp/cmp-uwsgi.ini:/opt/opsany/uwsgi/cmp.ini \
       -v ${INSTALL_PATH}/conf/opsany-saas/cmp/cmp-init.py:/opt/opsany/cmp/config/__init__.py \
       -v ${INSTALL_PATH}/conf/opsany-saas/cmp/cmp-prod.py:/opt/opsany/cmp/config/prod.py \
       -v ${INSTALL_PATH}/conf/opsany-saas/cmp/cmp-nginx.conf:/etc/nginx/http.d/default.conf \
       -v ${INSTALL_PATH}/conf/opsany-saas/cmp/cmp-nginx-main.conf:/etc/nginx/nginx.conf \
       -v ${INSTALL_PATH}/logs/cmp:/opt/opsany/logs/cmp \
       -v ${INSTALL_PATH}/uploads:/opt/opsany/uploads \
       -v /etc/localtime:/etc/localtime:ro \
       ${PAAS_DOCKER_REG}/opsany-saas-ce-cmp:${UPDATE_VERSION}
    
    # Django migrate
    docker exec -e BK_ENV="production" opsany-saas-ce-cmp /bin/sh -c \
    "python /opt/opsany/cmp/manage.py migrate --noinput >> ${SHELL_LOG} && python /opt/opsany/cmp/manage.py createcachetable django_cache > /dev/null"
    update_saas_version cmp 云管平台 ${CMP_SECRET_KEY}
}

saas_bastion_update(){
    shell_log "======Update bastion======"

    # Bastion Configure
    UPDATE_VERSION=$1
    BASTION_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.bastion_secret_key)
    /bin/cp conf/opsany-saas/bastion/* ${INSTALL_PATH}/conf/opsany-saas/bastion/
    sed -i "s/DOMAIN_NAME/${DOMAIN_NAME}/g" ${INSTALL_PATH}/conf/opsany-saas/bastion/bastion-init.py
    sed -i "s/BASTION_SECRET_KEY/${BASTION_SECRET_KEY}/g" ${INSTALL_PATH}/conf/opsany-saas/bastion/bastion-init.py
    sed -i "s/MYSQL_SERVER_IP/${MYSQL_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/bastion/bastion-prod.py
    sed -i "s/MYSQL_SERVER_PORT/${MYSQL_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/bastion/bastion-prod.py
    sed -i "s/MYSQL_OPSANY_BASTION_PASSWORD/${MYSQL_OPSANY_BASTION_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/bastion/bastion-prod.py
    sed -i "s/REDIS_SERVER_IP/${REDIS_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/bastion/bastion-prod.py
    sed -i "s/REDIS_SERVER_PORT/${REDIS_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/bastion/bastion-prod.py
    sed -i "s/REDIS_SERVER_USER/${REDIS_SERVER_USER}/g" ${INSTALL_PATH}/conf/opsany-saas/bastion/bastion-prod.py
    sed -i "s/REDIS_SERVER_PASSWORD/${REDIS_SERVER_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/bastion/bastion-prod.py
    sed -i "s/BASTION_FOOT_CLIENT_IP/${DOMAIN_NAME}/g" ${INSTALL_PATH}/conf/opsany-saas/bastion/bastion-prod.py
    sed -i "s/BASTION_FOOT_CLIENT_PORT/8013/g" ${INSTALL_PATH}/conf/opsany-saas/bastion/bastion-prod.py

    # Starter container
    docker pull ${PAAS_DOCKER_REG}/opsany-saas-ce-bastion:${UPDATE_VERSION}
    docker stop opsany-saas-ce-bastion && docker rm opsany-saas-ce-bastion
    docker run -d --restart=always --name opsany-saas-ce-bastion \
       -p 7008:80 \
       -v ${INSTALL_PATH}/conf/opsany-saas/bastion/bastion-supervisor.ini:/etc/supervisord.d/bastion.ini \
       -v ${INSTALL_PATH}/conf/opsany-saas/bastion/bastion-uwsgi.ini:/opt/opsany/uwsgi/bastion.ini \
       -v ${INSTALL_PATH}/conf/opsany-saas/bastion/bastion-init.py:/opt/opsany/bastion/config/__init__.py \
       -v ${INSTALL_PATH}/conf/opsany-saas/bastion/bastion-prod.py:/opt/opsany/bastion/config/prod.py \
       -v ${INSTALL_PATH}/conf/opsany-saas/bastion/bastion-nginx.conf:/etc/nginx/http.d/default.conf \
       -v ${INSTALL_PATH}/conf/opsany-saas/bastion/bastion-nginx-main.conf:/etc/nginx/nginx.conf \
       -v ${INSTALL_PATH}/logs:/opt/opsany/logs \
       -v ${INSTALL_PATH}/uploads:/opt/opsany/uploads \
       -v /etc/localtime:/etc/localtime:ro \
       ${PAAS_DOCKER_REG}/opsany-saas-ce-bastion:${UPDATE_VERSION}
    
    # Django migrate
    docker exec -e BK_ENV="production" opsany-saas-ce-bastion /bin/sh -c \
    "python /opt/opsany/bastion/manage.py migrate --noinput >> ${SHELL_LOG} && python /opt/opsany/bastion/manage.py createcachetable django_cache > /dev/null"
    update_saas_version bastion 堡垒机 ${BASTION_SECRET_KEY}
}

saas_devops_update(){
    shell_log "======Update devops======"

    # DevOps Configure
    UPDATE_VERSION=$1
    DEVOPS_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.devops_secret_key)
    /bin/cp conf/opsany-saas/devops/* ${INSTALL_PATH}/conf/opsany-saas/devops/
    sed -i "s/DOMAIN_NAME/${DOMAIN_NAME}/g" ${INSTALL_PATH}/conf/opsany-saas/devops/devops-init.py
    sed -i "s/DEVOPS_SECRET_KEY/${DEVOPS_SECRET_KEY}/g" ${INSTALL_PATH}/conf/opsany-saas/devops/devops-init.py
    sed -i "s/MYSQL_SERVER_IP/${MYSQL_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/devops/devops-prod.py
    sed -i "s/MYSQL_SERVER_PORT/${MYSQL_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/devops/devops-prod.py
    sed -i "s/MYSQL_OPSANY_DEVOPS_PASSWORD/${MYSQL_OPSANY_DEVOPS_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/devops/devops-prod.py
    sed -i "s/MONGO_SERVER_IP/${MONGO_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/devops/devops-prod.py
    sed -i "s/MONGO_SERVER_PORT/${MONGO_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/devops/devops-prod.py
    sed -i "s/MONGO_DEVOPS_PASSWORD/${MONGO_DEVOPS_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/devops/devops-prod.py
    sed -i "s/REDIS_SERVER_IP/${REDIS_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/devops/devops-prod.py
    sed -i "s/REDIS_SERVER_PORT/${REDIS_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/devops/devops-prod.py
    sed -i "s/REDIS_SERVER_USER/${REDIS_SERVER_USER}/g" ${INSTALL_PATH}/conf/opsany-saas/devops/devops-prod.py
    sed -i "s/REDIS_SERVER_PASSWORD/${REDIS_SERVER_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/devops/devops-prod.py
    
    # Starter container   
    docker pull ${PAAS_DOCKER_REG}/opsany-saas-ce-devops:${UPDATE_VERSION}
    docker stop opsany-saas-ce-devops && docker rm opsany-saas-ce-devops
    docker run -d --restart=always --name opsany-saas-ce-devops \
       -p 7009:80 \
       -v ${INSTALL_PATH}/conf/opsany-saas/devops/devops-supervisor.ini:/etc/supervisord.d/devops.ini \
       -v ${INSTALL_PATH}/conf/opsany-saas/devops/devops-uwsgi.ini:/opt/opsany/uwsgi/devops.ini \
       -v ${INSTALL_PATH}/conf/opsany-saas/devops/devops-init.py:/opt/opsany/devops/config/__init__.py \
       -v ${INSTALL_PATH}/conf/opsany-saas/devops/devops-prod.py:/opt/opsany/devops/config/prod.py \
       -v ${INSTALL_PATH}/conf/opsany-saas/devops/devops-nginx.conf:/etc/nginx/http.d/default.conf \
       -v ${INSTALL_PATH}/conf/opsany-saas/devops/devops-nginx-main.conf:/etc/nginx/nginx.conf \
       -v ${INSTALL_PATH}/logs:/opt/opsany/logs \
       -v ${INSTALL_PATH}/uploads:/opt/opsany/uploads \
       -v /etc/localtime:/etc/localtime:ro \
       ${PAAS_DOCKER_REG}/opsany-saas-ce-devops:${UPDATE_VERSION}
        # Django migrate
    docker exec -e BK_ENV="production" opsany-saas-ce-devops /bin/sh -c \
    "python /opt/opsany/devops/manage.py migrate --noinput >> ${SHELL_LOG} && python /opt/opsany/devops/manage.py createcachetable django_cache > /dev/null"
    update_saas_version devops 应用平台 ${DEVOPS_SECRET_KEY}
}

saas_pipeline_update(){
    shell_log "======Update pipeline======"
    # Modify configuration
    /bin/cp -r ./conf/opsany-saas/pipeline/* ${INSTALL_PATH}/conf/opsany-saas/pipeline/
    PIPELINE_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.pipeline_secret_key)
    sed -i "s/DOMAIN_NAME/${DOMAIN_NAME}/g" ${INSTALL_PATH}/conf/opsany-saas/pipeline/pipeline-init.py
    sed -i "s/PIPELINE_SECRET_KEY/${PIPELINE_SECRET_KEY}/g" ${INSTALL_PATH}/conf/opsany-saas/pipeline/pipeline-init.py
    sed -i "s/MYSQL_SERVER_IP/${MYSQL_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/pipeline/pipeline-prod.py
    sed -i "s/MYSQL_SERVER_PORT/${MYSQL_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/pipeline/pipeline-prod.py
    sed -i "s/MYSQL_OPSANY_PIPELINE_PASSWORD/${MYSQL_OPSANY_PIPELINE_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/pipeline/pipeline-prod.py
    sed -i "s/MONGO_SERVER_IP/${MONGO_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/pipeline/pipeline-prod.py
    sed -i "s/MONGO_SERVER_PORT/${MONGO_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/pipeline/pipeline-prod.py
    sed -i "s/MONGO_DEVOPS_PASSWORD/${MONGO_DEVOPS_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/pipeline/pipeline-prod.py
    sed -i "s/REDIS_SERVER_IP/${REDIS_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/pipeline/pipeline-prod.py
    sed -i "s/REDIS_SERVER_PORT/${REDIS_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/pipeline/pipeline-prod.py
    sed -i "s/REDIS_SERVER_USER/${REDIS_SERVER_USER}/g" ${INSTALL_PATH}/conf/opsany-saas/pipeline/pipeline-prod.py
    sed -i "s/REDIS_SERVER_PASSWORD/${REDIS_SERVER_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/pipeline/pipeline-prod.py

    # Starter container
    docker pull ${PAAS_DOCKER_REG}/opsany-saas-ce-pipeline:${UPDATE_VERSION}
    docker stop opsany-saas-ce-pipeline && docker rm opsany-saas-ce-pipeline
    docker run -d --restart=always --name opsany-saas-ce-pipeline \
       -p 7017:80 \
       -v ${INSTALL_PATH}/conf/opsany-saas/pipeline/pipeline-supervisor.ini:/etc/supervisord.d/pipeline.ini \
       -v ${INSTALL_PATH}/conf/opsany-saas/pipeline/pipeline-uwsgi.ini:/opt/opsany/uwsgi/pipeline.ini \
       -v ${INSTALL_PATH}/conf/opsany-saas/pipeline/pipeline-init.py:/opt/opsany/pipeline/config/__init__.py \
       -v ${INSTALL_PATH}/conf/opsany-saas/pipeline/pipeline-prod.py:/opt/opsany/pipeline/config/prod.py \
       -v ${INSTALL_PATH}/conf/opsany-saas/pipeline/pipeline-nginx.conf:/etc/nginx/http.d/default.conf \
       -v ${INSTALL_PATH}/conf/opsany-saas/pipeline/pipeline-nginx-main.conf:/etc/nginx/nginx.conf \
       -v ${INSTALL_PATH}/logs/pipeline:/opt/opsany/logs/pipeline \
       -v ${INSTALL_PATH}/uploads:/opt/opsany/uploads \
       -v /etc/localtime:/etc/localtime:ro \
       ${PAAS_DOCKER_REG}/opsany-saas-ce-pipeline:${UPDATE_VERSION}
    
    # Django migrate
    docker exec -e BK_ENV="production" opsany-saas-ce-pipeline /bin/sh -c \
    "python /opt/opsany/pipeline/manage.py migrate --noinput >> ${SHELL_LOG} && python /opt/opsany/pipeline/manage.py createcachetable django_cache > /dev/null"
    update_saas_version pipeline 流水线 ${PIPELINE_SECRET_KEY}
}

saas_deploy_update(){
    shell_log "======Update deploy======"
    # Modify configuration
    /bin/cp -r ./conf/opsany-saas/deploy/* ${INSTALL_PATH}/conf/opsany-saas/deploy/
    DEPLOY_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.deploy_secret_key)
    sed -i "s/DOMAIN_NAME/${DOMAIN_NAME}/g" ${INSTALL_PATH}/conf/opsany-saas/deploy/deploy-init.py
    sed -i "s/DEPLOY_SECRET_KEY/${DEPLOY_SECRET_KEY}/g" ${INSTALL_PATH}/conf/opsany-saas/deploy/deploy-init.py
    sed -i "s/MYSQL_SERVER_IP/${MYSQL_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/deploy/deploy-prod.py
    sed -i "s/MYSQL_SERVER_PORT/${MYSQL_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/deploy/deploy-prod.py
    sed -i "s/MYSQL_OPSANY_DEPLOY_PASSWORD/${MYSQL_OPSANY_DEPLOY_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/deploy/deploy-prod.py
    sed -i "s/MONGO_SERVER_IP/${MONGO_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/deploy/deploy-prod.py
    sed -i "s/MONGO_SERVER_PORT/${MONGO_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/deploy/deploy-prod.py
    sed -i "s/MONGO_DEVOPS_PASSWORD/${MONGO_DEVOPS_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/deploy/deploy-prod.py
    sed -i "s/REDIS_SERVER_IP/${REDIS_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/deploy/deploy-prod.py
    sed -i "s/REDIS_SERVER_PORT/${REDIS_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/deploy/deploy-prod.py
    sed -i "s/REDIS_SERVER_USER/${REDIS_SERVER_USER}/g" ${INSTALL_PATH}/conf/opsany-saas/deploy/deploy-prod.py
    sed -i "s/REDIS_SERVER_PASSWORD/${REDIS_SERVER_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/deploy/deploy-prod.py

    # Starter container
    docker pull ${PAAS_DOCKER_REG}/opsany-saas-ce-deploy:${UPDATE_VERSION}
    docker stop opsany-saas-ce-deploy && docker rm opsany-saas-ce-deploy
    docker run -d --restart=always --name opsany-saas-ce-deploy \
       -p 7018:80 \
       -v ${INSTALL_PATH}/conf/opsany-saas/deploy/deploy-supervisor.ini:/etc/supervisord.d/deploy.ini \
       -v ${INSTALL_PATH}/conf/opsany-saas/deploy/deploy-uwsgi.ini:/opt/opsany/uwsgi/deploy.ini \
       -v ${INSTALL_PATH}/conf/opsany-saas/deploy/deploy-init.py:/opt/opsany/deploy/config/__init__.py \
       -v ${INSTALL_PATH}/conf/opsany-saas/deploy/deploy-prod.py:/opt/opsany/deploy/config/prod.py \
       -v ${INSTALL_PATH}/conf/opsany-saas/deploy/deploy-nginx.conf:/etc/nginx/http.d/default.conf \
       -v ${INSTALL_PATH}/conf/opsany-saas/deploy/deploy-nginx-main.conf:/etc/nginx/nginx.conf \
       -v ${INSTALL_PATH}/logs/deploy:/opt/opsany/logs/deploy \
       -v ${INSTALL_PATH}/uploads:/opt/opsany/uploads \
       -v /etc/localtime:/etc/localtime:ro \
       ${PAAS_DOCKER_REG}/opsany-saas-ce-deploy:${UPDATE_VERSION}
    
    # Django migrate
    docker exec -e BK_ENV="production" opsany-saas-ce-deploy /bin/sh -c \
    "python /opt/opsany/deploy/manage.py migrate --noinput >> ${SHELL_LOG} && python /opt/opsany/deploy/manage.py createcachetable django_cache > /dev/null"
    update_saas_version deploy 持续部署 ${DEPLOY_SECRET_KEY}
}

saas_repo_update(){
    shell_log "======Update repo======"
    # Modify configuration
    /bin/cp -r ./conf/opsany-saas/repo/* ${INSTALL_PATH}/conf/opsany-saas/repo/
    REPO_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.repo_secret_key)
    # repo Configure
    sed -i "s/DOMAIN_NAME/${DOMAIN_NAME}/g" ${INSTALL_PATH}/conf/opsany-saas/repo/repo-init.py
    sed -i "s/REPO_SECRET_KEY/${REPO_SECRET_KEY}/g" ${INSTALL_PATH}/conf/opsany-saas/repo/repo-init.py
    sed -i "s/MYSQL_SERVER_IP/${MYSQL_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/repo/repo-prod.py
    sed -i "s/MYSQL_SERVER_PORT/${MYSQL_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/repo/repo-prod.py
    sed -i "s/MYSQL_OPSANY_REPO_PASSWORD/${MYSQL_OPSANY_REPO_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/repo/repo-prod.py
    sed -i "s/MONGO_SERVER_IP/${MONGO_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/repo/repo-prod.py
    sed -i "s/MONGO_SERVER_PORT/${MONGO_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/repo/repo-prod.py
    sed -i "s/MONGO_DEVOPS_PASSWORD/${MONGO_DEVOPS_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/repo/repo-prod.py
    sed -i "s/REDIS_SERVER_IP/${REDIS_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/repo/repo-prod.py
    sed -i "s/REDIS_SERVER_PORT/${REDIS_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/repo/repo-prod.py
    sed -i "s/REDIS_SERVER_USER/${REDIS_SERVER_USER}/g" ${INSTALL_PATH}/conf/opsany-saas/repo/repo-prod.py
    sed -i "s/REDIS_SERVER_PASSWORD/${REDIS_SERVER_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/repo/repo-prod.py
    sed -i "s#REPO_HARBOR_URL#${REPO_HARBOR_URL}#g" ${INSTALL_PATH}/conf/opsany-saas/repo/repo-prod.py
    sed -i "s/REPO_HARBOR_USERNAME/${REPO_HARBOR_USERNAME}/g" ${INSTALL_PATH}/conf/opsany-saas/repo/repo-prod.py
    sed -i "s/REPO_HARBOR_PASSWORD/${REPO_HARBOR_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/repo/repo-prod.py

    # Starter container
    docker pull ${PAAS_DOCKER_REG}/opsany-saas-ce-repo:${UPDATE_VERSION}
    docker stop opsany-saas-ce-repo && docker rm opsany-saas-ce-repo
    docker run -d --restart=always --name opsany-saas-ce-repo \
       -p 7020:80 \
       -v ${INSTALL_PATH}/conf/opsany-saas/repo/repo-supervisor.ini:/etc/supervisord.d/repo.ini \
       -v ${INSTALL_PATH}/conf/opsany-saas/repo/repo-uwsgi.ini:/opt/opsany/uwsgi/repo.ini \
       -v ${INSTALL_PATH}/conf/opsany-saas/repo/repo-init.py:/opt/opsany/repo/config/__init__.py \
       -v ${INSTALL_PATH}/conf/opsany-saas/repo/repo-prod.py:/opt/opsany/repo/config/prod.py \
       -v ${INSTALL_PATH}/conf/opsany-saas/repo/repo-nginx.conf:/etc/nginx/http.d/default.conf \
       -v ${INSTALL_PATH}/conf/opsany-saas/repo/repo-nginx-main.conf:/etc/nginx/nginx.conf \
       -v ${INSTALL_PATH}/logs:/opt/opsany/logs \
       -v ${INSTALL_PATH}/uploads:/opt/opsany/uploads \
       -v /etc/localtime:/etc/localtime:ro \
       ${PAAS_DOCKER_REG}/opsany-saas-ce-repo:${UPDATE_VERSION}
    
    # Django migrate
    docker exec -e BK_ENV="production" opsany-saas-ce-repo /bin/sh -c \
    "python /opt/opsany/repo/manage.py migrate --noinput && python /opt/opsany/repo/manage.py createcachetable django_cache > /dev/null" >> ${SHELL_LOG}
    update_saas_version repo 制品仓库 ${REPO_SECRET_KEY}
}


saas_code_update(){
    shell_log "======Update code======"

    # Dashboard Configure
    UPDATE_VERSION=$1
    CODE_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.code_secret_key)
    /bin/cp conf/opsany-saas/code/* ${INSTALL_PATH}/conf/opsany-saas/code/
    sed -i "s/DOMAIN_NAME/${DOMAIN_NAME}/g" ${INSTALL_PATH}/conf/opsany-saas/code/code-init.py
    sed -i "s/CODE_SECRET_KEY/${CODE_SECRET_KEY}/g" ${INSTALL_PATH}/conf/opsany-saas/code/code-init.py
    sed -i "s/MYSQL_SERVER_IP/${MYSQL_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/code/code-prod.py
    sed -i "s/MYSQL_SERVER_PORT/${MYSQL_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/code/code-prod.py
    sed -i "s/MYSQL_OPSANY_CODE_PASSWORD/${MYSQL_OPSANY_CODE_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/code/code-prod.py

    # Starter container
    docker pull ${PAAS_DOCKER_REG}/opsany-saas-ce-code:${UPDATE_VERSION}
    docker stop opsany-saas-ce-code && docker rm opsany-saas-ce-code
    docker run -d --restart=always --name opsany-saas-ce-code \
       -p 7010:80 \
       -v ${INSTALL_PATH}/conf/opsany-saas/code/code-supervisor.ini:/etc/supervisord.d/code.ini \
       -v ${INSTALL_PATH}/conf/opsany-saas/code/code-uwsgi.ini:/opt/opsany/uwsgi/code.ini \
       -v ${INSTALL_PATH}/conf/opsany-saas/code/code-init.py:/opt/opsany/code/config/__init__.py \
       -v ${INSTALL_PATH}/conf/opsany-saas/code/code-prod.py:/opt/opsany/code/config/prod.py \
       -v ${INSTALL_PATH}/conf/opsany-saas/code/code-nginx.conf:/etc/nginx/http.d/default.conf \
       -v ${INSTALL_PATH}/conf/opsany-saas/code/code-nginx-main.conf:/etc/nginx/nginx.conf \
       -v ${INSTALL_PATH}/logs:/opt/opsany/logs \
       -v ${INSTALL_PATH}/uploads:/opt/opsany/uploads \
       -v /etc/localtime:/etc/localtime:ro \
       ${PAAS_DOCKER_REG}/opsany-saas-ce-code:${UPDATE_VERSION}

    # Django migrate
    docker exec -e BK_ENV="production" opsany-saas-ce-code /bin/sh -c \
    "python /opt/opsany/code/manage.py migrate --noinput >> ${SHELL_LOG} && python /opt/opsany/code/manage.py createcachetable django_cache > /dev/null"
    update_saas_version code 代码仓库 ${CODE_SECRET_KEY}
}

# $1 rbac $2 统一权限 $3 ${RBAC_SECRET_KEY}
update_saas_version(){
      docker exec opsany-paas-websocket /bin/sh -c "python3 /opt/opsany/saas/register_online_saas.py --paas_domain https://${DOMAIN_NAME} --username admin --password ${ADMIN_PASSWORD} --saas_app_code $1 --saas_app_name $2 --saas_app_version ${UPDATE_VERSION} --saas_app_secret_key $3 --is_update true"
}


# Main
main(){
    UPDATE_VERSION=$2
    case "$1" in
	base)
	    saas_rbac_update $2
	    saas_workbench_update $2
	    saas_cmdb_update $2
	    saas_control_update $2
	    saas_job_update $2
	    saas_cmp_update $2
	    saas_bastion_update $2
        saas_monitor_update $2
		;;
    paas)
        paas_update $2
        ;;
    login)
        login_update $2
        ;;
    esb)
        esb_update $2
        ;;
    websocket)
        websocket_update $2
        ;;
    appengine)
        appengine_update $2
        ;;
    proxy)
        proxy_update $2
        ;;
    rbac)
        saas_rbac_update $2
	    ;;
    workbench)
        saas_workbench_update $2
	    ;;
    cmdb)
        saas_cmdb_update $2
	    ;;
    control)
        saas_control_update $2
	    ;;
    job)
        saas_job_update $2
	    ;;
	monitor)
	    saas_monitor_update $2
	    ;;
	devops)
	    saas_devops_update $2
	    ;;
    pipeline)
	    saas_pipeline_update $2
	    ;;
	deploy)
	    saas_deploy_update $2
	    ;;
	repo)
	    saas_repo_update $2
	    ;;
    code)
	    saas_code_update $2
	    ;;
    cmp)
        saas_cmp_update $2
	    ;;
    llmops)
        saas_llmops_update $2
	    ;;
    bastion)
        saas_bastion_update $2
	    ;;
    websocket)
        websocket_update $2
        ;;
    ops)
	    saas_rbac_update $2
	    saas_workbench_update $2
	    saas_cmdb_update $2
	    saas_control_update $2
	    saas_job_update $2
	    saas_cmp_update $2
	    saas_bastion_update $2
        saas_monitor_update $2
        saas_llmops_update $2
		;;
    dev)
        saas_devops_update $2
        saas_pipeline_update $2
        saas_deploy_update $2
        saas_repo_update $2
        #saas_code_update $2
        ;;
    all)
	    saas_rbac_update $2
	    saas_workbench_update $2
	    saas_cmdb_update $2
	    saas_control_update $2
	    saas_job_update $2
	    saas_cmp_update $2
	    saas_bastion_update $2
        saas_monitor_update $2
        saas_devops_update $2
        saas_pipeline_update $2
        saas_deploy_update $2
        saas_repo_update $2
        saas_llmops_update $2
        ;;
	help|*)
	    echo $"Usage: $0 {(paas|login|esb|appengine|proxy|websocket|rbac|workbench|cmdb|control|job|cmp|bastion|base|monitor|devops|all|help) version}"
	    ;;
    esac
}

main $1 $2
