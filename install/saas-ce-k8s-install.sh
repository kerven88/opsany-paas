#!/bin/bash
#******************************************
# Author:       Jason Zhao
# Email:        zhaoshundong@opsany.com
# Organization: OpsAny https://www.opsany.com/
# Description:  OpsAny SAAS Community Edition Install Script for Kubernetes
#******************************************

# Data/Time Variables
CTIME=$(date "+%Y-%m-%d-%H-%M")

# Shell Envionment Variables
CDIR=$(pwd)
SHELL_NAME="saas-ce-k8s-install.sh"
SHELL_LOG="${SHELL_NAME}.log"
ADMIN_PASSWORD="admin"

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
if [ ! -f ./install-k8s.config ];then
      shell_error_log "Please Change Directory to ${INSTALL_PATH}/install"
      exit
else
    grep '^[A-Z]' install-k8s.config > install.env
    source ./install.env && rm -f install.env
fi

# Install initialization
install_init(){
    #SaaS Log Directory
    mkdir -p /data/k8s-nfs/opsany-logs/{rbac,workbench,cmdb,control,job,monitor,cmp,bastion,code,devops,pipeline,repo,deploy,llmops}

    # Register rbac
    if [ -f ${INSTALL_PATH}/conf/.rbac_secret_key ];then
        RBAC_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.rbac_secret_key)
    else
        RBAC_SECRET_KEY=$(uuid -v4)
        echo $RBAC_SECRET_KEY > ${INSTALL_PATH}/conf/.rbac_secret_key
    fi
    python3 ../saas/register_online_saas.py --paas_domain https://${DOMAIN_NAME} --username admin --password ${ADMIN_PASSWORD} --saas_app_code rbac --saas_app_name 统一权限 --saas_app_version 2.2.1 --saas_app_secret_key ${RBAC_SECRET_KEY}

    # Register workbench
    if [ -f ${INSTALL_PATH}/conf/.workbench_secret_key ];then
        WORKBENCH_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.workbench_secret_key)
    else
        WORKBENCH_SECRET_KEY=$(uuid -v4)
        echo $WORKBENCH_SECRET_KEY > ${INSTALL_PATH}/conf/.workbench_secret_key
    fi
    python3 ../saas/register_online_saas.py --paas_domain https://${DOMAIN_NAME} --username admin --password ${ADMIN_PASSWORD} --saas_app_code workbench --saas_app_name 工作台 --saas_app_version 2.2.1 --saas_app_secret_key ${WORKBENCH_SECRET_KEY}

    # Register cmdb
    if [ -f ${INSTALL_PATH}/conf/.cmdb_secret_key ];then
        CMDB_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.cmdb_secret_key)
    else
        CMDB_SECRET_KEY=$(uuid -v4)
        echo $CMDB_SECRET_KEY > ${INSTALL_PATH}/conf/.cmdb_secret_key
    fi
    python3 ../saas/register_online_saas.py --paas_domain https://${DOMAIN_NAME} --username admin --password ${ADMIN_PASSWORD} --saas_app_code cmdb --saas_app_name 资源平台 --saas_app_version 2.2.1 --saas_app_secret_key ${CMDB_SECRET_KEY}

    # Register control
    if [ -f ${INSTALL_PATH}/conf/.control_secret_key ];then
        CONTROL_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.control_secret_key)
    else
        CONTROL_SECRET_KEY=$(uuid -v4)
        echo $CONTROL_SECRET_KEY > ${INSTALL_PATH}/conf/.control_secret_key
    fi
    python3 ../saas/register_online_saas.py --paas_domain https://${DOMAIN_NAME} --username admin --password ${ADMIN_PASSWORD} --saas_app_code control --saas_app_name 管控平台 --saas_app_version 2.2.1 --saas_app_secret_key ${CONTROL_SECRET_KEY}
    
    # Register job
    if [ -f ${INSTALL_PATH}/conf/.job_secret_key ];then
        JOB_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.job_secret_key)
    else
        JOB_SECRET_KEY=$(uuid -v4)
        echo $JOB_SECRET_KEY > ${INSTALL_PATH}/conf/.job_secret_key
    fi
    python3 ../saas/register_online_saas.py --paas_domain https://${DOMAIN_NAME} --username admin --password ${ADMIN_PASSWORD} --saas_app_code job --saas_app_name 作业平台 --saas_app_version 2.2.1 --saas_app_secret_key ${JOB_SECRET_KEY}

    # Register monitor
    if [ -f ${INSTALL_PATH}/conf/.monitor_secret_key ];then
        MONITOR_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.monitor_secret_key)
    else
        MONITOR_SECRET_KEY=$(uuid -v4)
        echo $MONITOR_SECRET_KEY > ${INSTALL_PATH}/conf/.monitor_secret_key
    fi
    python3 ../saas/register_online_saas.py --paas_domain https://${DOMAIN_NAME} --username admin --password ${ADMIN_PASSWORD} --saas_app_code monitor --saas_app_name 基础监控 --saas_app_version 2.2.1 --saas_app_secret_key ${MONITOR_SECRET_KEY}

    # Register cmp
    if [ -f ${INSTALL_PATH}/conf/.cmp_secret_key ];then
        CMP_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.cmp_secret_key)
    else
        CMP_SECRET_KEY=$(uuid -v4)
        echo $CMP_SECRET_KEY > ${INSTALL_PATH}/conf/.cmp_secret_key
    fi
    python3 ../saas/register_online_saas.py --paas_domain https://${DOMAIN_NAME} --username admin --password ${ADMIN_PASSWORD} --saas_app_code cmp --saas_app_name 云管平台 --saas_app_version 2.2.1 --saas_app_secret_key ${CMP_SECRET_KEY}

    # Register bastion
    if [ -f ${INSTALL_PATH}/conf/.bastion_secret_key ];then
        BASTION_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.bastion_secret_key)
    else
        BASTION_SECRET_KEY=$(uuid -v4)
        echo $BASTION_SECRET_KEY > ${INSTALL_PATH}/conf/.bastion_secret_key
    fi
    python3 ../saas/register_online_saas.py --paas_domain https://${DOMAIN_NAME} --username admin --password ${ADMIN_PASSWORD} --saas_app_code bastion --saas_app_name 堡垒机 --saas_app_version 2.2.1 --saas_app_secret_key ${BASTION_SECRET_KEY}

    # Register devops
    if [ -f ${INSTALL_PATH}/conf/.devops_secret_key ];then
        DEVOPS_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.devops_secret_key)
    else
        DEVOPS_SECRET_KEY=$(uuid -v4)
        echo $DEVOPS_SECRET_KEY > ${INSTALL_PATH}/conf/.devops_secret_key
    fi
    python3 ../saas/register_online_saas.py --paas_domain https://${DOMAIN_NAME} --username admin --password ${ADMIN_PASSWORD} --saas_app_code devops --saas_app_name 应用平台 --saas_app_version 2.2.1 --saas_app_secret_key ${DEVOPS_SECRET_KEY}

    # Register code
    if [ -f ${INSTALL_PATH}/conf/.code_secret_key ];then
        CODE_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.code_secret_key)
    else
        CODE_SECRET_KEY=$(uuid -v4)
        echo $CODE_SECRET_KEY > ${INSTALL_PATH}/conf/.code_secret_key
    fi
    python3 ../saas/register_online_saas.py --paas_domain https://${DOMAIN_NAME} --username admin --password ${ADMIN_PASSWORD} --saas_app_code code --saas_app_name 代码仓库 --saas_app_version 2.2.1 --saas_app_secret_key ${CODE_SECRET_KEY}

    # Register pipeline
    if [ -f ${INSTALL_PATH}/conf/.pipeline_secret_key ];then
        PIPELINE_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.pipeline_secret_key)
    else
        PIPELINE_SECRET_KEY=$(uuid -v4)
        echo $PIPELINE_SECRET_KEY > ${INSTALL_PATH}/conf/.pipeline_secret_key
    fi
    python3 ../saas/register_online_saas.py --paas_domain https://${DOMAIN_NAME} --username admin --password ${ADMIN_PASSWORD} --saas_app_code pipeline --saas_app_name 流水线 --saas_app_version 2.2.1 --saas_app_secret_key ${PIPELINE_SECRET_KEY}

    # Register repo
    if [ -f ${INSTALL_PATH}/conf/.repo_secret_key ];then
        REPO_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.repo_secret_key)
    else
        REPO_SECRET_KEY=$(uuid -v4)
        echo $REPO_SECRET_KEY > ${INSTALL_PATH}/conf/.repo_secret_key
    fi
    python3 ../saas/register_online_saas.py --paas_domain https://${DOMAIN_NAME} --username admin --password ${ADMIN_PASSWORD} --saas_app_code repo --saas_app_name 制品仓库 --saas_app_version 2.2.1 --saas_app_secret_key ${REPO_SECRET_KEY}

    # Register deploy
    if [ -f ${INSTALL_PATH}/conf/.deploy_secret_key ];then
        DEPLOY_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.deploy_secret_key)
    else
        DEPLOY_SECRET_KEY=$(uuid -v4)
        echo $DEPLOY_SECRET_KEY > ${INSTALL_PATH}/conf/.deploy_secret_key
    fi
    python3 ../saas/register_online_saas.py --paas_domain https://${DOMAIN_NAME} --username admin --password ${ADMIN_PASSWORD} --saas_app_code deploy --saas_app_name 持续部署 --saas_app_version 2.2.1 --saas_app_secret_key ${DEPLOY_SECRET_KEY}

    # Register llmops
    if [ -f ${INSTALL_PATH}/conf/.llmops_secret_key ];then
        LLMOPS_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.llmops_secret_key)
    else
        LLMOPS_SECRET_KEY=$(uuid -v4)
        echo $LLMOPS_SECRET_KEY > ${INSTALL_PATH}/conf/.llmops_secret_key
    fi
    python3 ../saas/register_online_saas.py --paas_domain https://${DOMAIN_NAME} --username admin --password ${ADMIN_PASSWORD} --saas_app_code llmops --saas_app_name 大模型开发平台 --saas_app_version 2.3.0 --saas_app_secret_key ${LLMOPS_SECRET_KEY}
}

# SaaS Deploy
saas_rbac_deploy(){
    shell_log "======Config RBAC======"
    # Modify configuration
    RBAC_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.rbac_secret_key)
    sed -i "s/DOMAIN_NAME/${DOMAIN_NAME}/g" ${INSTALL_PATH}/conf/opsany-saas/rbac/rbac-init.py
    sed -i "s/RBAC_SECRET_KEY/${RBAC_SECRET_KEY}/g" ${INSTALL_PATH}/conf/opsany-saas/rbac/rbac-init.py
    sed -i "s/MYSQL_SERVER_IP/${MYSQL_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/rbac/rbac-prod.py
    sed -i "s/MYSQL_SERVER_PORT/${MYSQL_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/rbac/rbac-prod.py
    sed -i "s/MYSQL_OPSANY_RBAC_PASSWORD/${MYSQL_OPSANY_RBAC_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/rbac/rbac-prod.py
    sed -i "s/REDIS_SERVER_IP/${REDIS_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/rbac/rbac-prod.py
    sed -i "s/REDIS_SERVER_PORT/${REDIS_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/rbac/rbac-prod.py
    sed -i "s/REDIS_SERVER_USER/${REDIS_SERVER_USER}/g" ${INSTALL_PATH}/conf/opsany-saas/rbac/rbac-prod.py
    sed -i "s/REDIS_SERVER_PASSWORD/${REDIS_SERVER_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/rbac/rbac-prod.py
    /bin/cp ${INSTALL_PATH}/conf/opsany-saas/rbac/*  ${INSTALL_PATH}/kubernetes/helm/opsany-saas/opsany-saas-rbac/
}

saas_workbench_deploy(){
    shell_log "======Config workbench======"
    # Modify configuration
    WORKBENCH_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.workbench_secret_key)
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
    /bin/cp ${INSTALL_PATH}/conf/opsany-saas/workbench/*  ${INSTALL_PATH}/kubernetes/helm/opsany-saas/opsany-saas-workbench/
}

saas_cmdb_deploy(){
    shell_log "======Config cmdb======"
    # Modify configuration
    CMDB_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.cmdb_secret_key)
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
    /bin/cp ${INSTALL_PATH}/conf/opsany-saas/cmdb/*  ${INSTALL_PATH}/kubernetes/helm/opsany-saas/opsany-saas-cmdb/
}

saas_control_deploy(){
    shell_log "======Config control======"
    # Modify configuration
    CONTROL_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.control_secret_key)
    sed -i "s/DOMAIN_NAME/${DOMAIN_NAME}/g" ${INSTALL_PATH}/conf/opsany-saas/control/control-init.py
    sed -i "s/CONTROL_SECRET_KEY/${CONTROL_SECRET_KEY}/g" ${INSTALL_PATH}/conf/opsany-saas/control/control-init.py
    sed -i "s/MYSQL_SERVER_IP/${MYSQL_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/control/control-prod.py
    sed -i "s/MYSQL_SERVER_PORT/${MYSQL_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/control/control-prod.py
    sed -i "s/MYSQL_OPSANY_CONTROL_PASSWORD/${MYSQL_OPSANY_CONTROL_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/control/control-prod.py
    sed -i "s/REDIS_SERVER_IP/${REDIS_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/control/control-prod.py
    sed -i "s/REDIS_SERVER_PORT/${REDIS_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/control/control-prod.py
    sed -i "s/REDIS_SERVER_USER/${REDIS_SERVER_USER}/g" ${INSTALL_PATH}/conf/opsany-saas/control/control-prod.py
    sed -i "s/REDIS_SERVER_PASSWORD/${REDIS_SERVER_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/control/control-prod.py
    /bin/cp ${INSTALL_PATH}/conf/opsany-saas/control/*  ${INSTALL_PATH}/kubernetes/helm/opsany-saas/opsany-saas-control/
}

saas_job_deploy(){
    shell_log "======Config job======"

    # Modify configuration
    JOB_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.job_secret_key)
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
    /bin/cp ${INSTALL_PATH}/conf/opsany-saas/job/*  ${INSTALL_PATH}/kubernetes/helm/opsany-saas/opsany-saas-job/
}

saas_monitor_deploy(){
    shell_log "======Config monitor======"
    # Modify configuration
    MONITOR_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.monitor_secret_key)
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
    /bin/cp ${INSTALL_PATH}/conf/opsany-saas/monitor/*  ${INSTALL_PATH}/kubernetes/helm/opsany-saas/opsany-saas-monitor/
}

saas_cmp_deploy(){
    shell_log "======Config cmp======"
    #CMP Configure
    CMP_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.cmp_secret_key)
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
    /bin/cp ${INSTALL_PATH}/conf/opsany-saas/cmp/*  ${INSTALL_PATH}/kubernetes/helm/opsany-saas/opsany-saas-cmp/
}

saas_bastion_deploy(){
    shell_log "======Config bastion======"
    # Register bastion
    BASTION_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.bastion_secret_key)
    # Bastion Configure
    sed -i "s/DOMAIN_NAME/${DOMAIN_NAME}/g" ${INSTALL_PATH}/conf/opsany-saas/bastion/bastion-init.py
    sed -i "s/BASTION_SECRET_KEY/${BASTION_SECRET_KEY}/g" ${INSTALL_PATH}/conf/opsany-saas/bastion/bastion-init.py
    sed -i "s/MYSQL_SERVER_IP/${MYSQL_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/bastion/bastion-prod.py
    sed -i "s/MYSQL_SERVER_PORT/${MYSQL_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/bastion/bastion-prod.py
    sed -i "s/MYSQL_OPSANY_BASTION_PASSWORD/${MYSQL_OPSANY_BASTION_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/bastion/bastion-prod.py
    sed -i "s/REDIS_SERVER_IP/${REDIS_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/bastion/bastion-prod.py
    sed -i "s/REDIS_SERVER_PORT/${REDIS_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/bastion/bastion-prod.py
    sed -i "s/REDIS_SERVER_USER/${REDIS_SERVER_USER}/g" ${INSTALL_PATH}/conf/opsany-saas/bastion/bastion-prod.py
    sed -i "s/REDIS_SERVER_PASSWORD/${REDIS_SERVER_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/bastion/bastion-prod.py
    /bin/cp ${INSTALL_PATH}/conf/opsany-saas/bastion/*  ${INSTALL_PATH}/kubernetes/helm/opsany-saas/opsany-saas-bastion/
}

saas_devops_deploy(){
    shell_log "======Config devops======"
    #DevOps MySQL
    # DevOps Configure
    DEVOPS_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.devops_secret_key)
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
    /bin/cp ${INSTALL_PATH}/conf/opsany-saas/devops/*  ${INSTALL_PATH}/kubernetes/helm/opsany-saas/opsany-saas-devops/
}

saas_code_deploy(){
    shell_log "======Config code======"
    # Code Configure
    CODE_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.code_secret_key)
    sed -i "s/DOMAIN_NAME/${DOMAIN_NAME}/g" ${INSTALL_PATH}/conf/opsany-saas/code/code-init.py
    sed -i "s/CODE_SECRET_KEY/${CODE_SECRET_KEY}/g" ${INSTALL_PATH}/conf/opsany-saas/code/code-init.py
    sed -i "s/MYSQL_SERVER_IP/${MYSQL_SERVER_IP}/g" ${INSTALL_PATH}/conf/opsany-saas/code/code-prod.py
    sed -i "s/MYSQL_SERVER_PORT/${MYSQL_SERVER_PORT}/g" ${INSTALL_PATH}/conf/opsany-saas/code/code-prod.py
    sed -i "s/MYSQL_OPSANY_CODE_PASSWORD/${MYSQL_OPSANY_CODE_PASSWORD}/g" ${INSTALL_PATH}/conf/opsany-saas/code/code-prod.py
    /bin/cp ${INSTALL_PATH}/conf/opsany-saas/code/*  ${INSTALL_PATH}/kubernetes/helm/opsany-saas/opsany-saas-code/
}

saas_pipeline_deploy(){
    shell_log "======Config pipeline======"
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
    /bin/cp ${INSTALL_PATH}/conf/opsany-saas/pipeline/*  ${INSTALL_PATH}/kubernetes/helm/opsany-saas/opsany-saas-pipeline/
}

saas_repo_deploy(){
    shell_log "======Config repo======"
    REPO_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.repo_secret_key)
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
    /bin/cp ${INSTALL_PATH}/conf/opsany-saas/repo/*  ${INSTALL_PATH}/kubernetes/helm/opsany-saas/opsany-saas-repo/
}

saas_deploy_deploy(){
    shell_log "======Config deploy======"
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
    /bin/cp ${INSTALL_PATH}/conf/opsany-saas/deploy/*  ${INSTALL_PATH}/kubernetes/helm/opsany-saas/opsany-saas-deploy/
}

saas_llmops_deploy(){
    shell_log "======Config llmops======"
    LLMOPS_SECRET_KEY=$(cat ${INSTALL_PATH}/conf/.llmops_secret_key)
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
    /bin/cp ${INSTALL_PATH}/conf/opsany-saas/llmops/*  ${INSTALL_PATH}/kubernetes/helm/opsany-saas/opsany-saas-llmops/
}

saas_init(){
    shell_log "======OpsAny User Initialize======"
    sleep 3
    # Sync User
    python3 ../saas/sync-user-script.py --domain https://${DOMAIN_NAME} --paas_username admin --paas_password ${ADMIN_PASSWORD} --app_code workbench cmdb control job cmp bastion
     python3 ../saas/init-ce-monitor.py --domain $DOMAIN_NAME --private_ip $DOMAIN_NAME --paas_username admin --paas_password ${ADMIN_PASSWORD} --grafana_password admin --grafana_change_password $GRAFANA_ADMIN_PASSWORD
     python3 ../saas/init-ce-devops.py --domain https://${DOMAIN_NAME} --username admin  --password $ADMIN_PASSWORD

    shell_log "======OpsAny Workbench Initialize======"
    # Create Service
    python3 ../saas/init_work_order.py --domain https://$DOMAIN_NAME --paas_username admin --paas_password ${ADMIN_PASSWORD}

    shell_log "======OpsAny Proxy Initialize======"
    # Create Proxy Token
    PROXY_POD=$(kubectl get pod -n opsany | grep opsany-paas-proxy | awk '{print $1}')
    PROXY_TOKEN=$(kubectl exec -n opsany ${PROXY_POD}  -- /bin/sh -c "export OPS_ANY_ENV=production && /usr/local/bin/python3 /opt/opsany-proxy/manage.py create_access" | grep 'Access' | awk -F ': ' '{print $2}' | awk -F '.' '{print $1}')
    python3 ../saas/init-ce-base.py --domain $DOMAIN_NAME --private_ip $LOCAL_IP --paas_username admin --paas_password ${ADMIN_PASSWORD} --proxy_url https://${PROXY_LOCAL_IP}:8011 --proxy_public_url https://${PROXY_PUBLIC_IP}:8011 --proxy_token $PROXY_TOKEN

    shell_log "======OpsAny Job Initialize======"
    # Init Script Job
    cd $CDIR/init/
    python3 import_script.py --domain https://${DOMAIN_NAME} --paas_username admin --paas_password ${ADMIN_PASSWORD} \
--target_type script --target_path ./job-script
    python3 import_script.py --domain https://$DOMAIN_NAME --paas_username admin --paas_password ${ADMIN_PASSWORD} \
--target_type task --target_path ./job-task
    shell_warning_log "======OpsAny: Make Ops Perfect======" 
}

admin_password_init(){
    PRESTR='Ops'
    STR=`head /dev/urandom | tr -dc A-Za-z0-9 | head -c 5`
    NUM=`echo $RANDOM`
    ADMIN_NEW_PASSWORD=$PRESTR$STR$NUM
    echo "ADMIN_PASSWORD=$ADMIN_NEW_PASSWORD" > ${INSTALL_PATH}/conf/.passwd_env
    cd ${CDIR}
    python3 password-init.py --paas_domain https://$DOMAIN_NAME --username admin --password ${ADMIN_PASSWORD} --new_password $ADMIN_NEW_PASSWORD
    shell_error_log "Web: https://$DOMAIN_NAME Username: admin Password: $ADMIN_NEW_PASSWORD"
}

# Main
main(){
    case "$1" in
    install)
        install_init
	    saas_rbac_deploy
	    saas_workbench_deploy
	    saas_cmdb_deploy
	    saas_control_deploy
	    saas_job_deploy
	    saas_cmp_deploy
	    saas_bastion_deploy
        saas_monitor_deploy
        saas_devops_deploy
        saas_code_deploy
        saas_pipeline_deploy
        saas_repo_deploy
        saas_deploy_deploy
        saas_llmops_deploy
        ;;
    config)
        saas_rbac_deploy
	    saas_workbench_deploy
	    saas_cmdb_deploy
	    saas_control_deploy
	    saas_job_deploy
	    saas_cmp_deploy
	    saas_bastion_deploy
        saas_monitor_deploy
        saas_devops_deploy
        saas_code_deploy
        saas_pipeline_deploy
        saas_repo_deploy
        saas_deploy_deploy
        saas_llmops_deploy
        ;;
    init)
        saas_init
        admin_password_init
        ;;
	help|*)
	    echo $"Usage: $0 {install|help}"
	    ;;
    esac
}

main $1 
