#!/bin/bash
#******************************************
# Author:       Jason Zhao
# Email:        zhaoshundong@opsany.com
# Organization: OpsAny https://www.opsany.com/
# Description:  OpsAI Install Script
#******************************************

# Data/Time
CTIME=$(date "+%Y-%m-%d-%H-%M")

# Shell Envionment Variables
CDIR=$(pwd)
SHELL_NAME="llmops-install.sh"
SHELL_LOG="${SHELL_NAME}.log"
INSTALL_PATH="/data/opsany"

# Shell Log Record
shell_log(){
    LOG_INFO=$1
    echo "----------------$CTIME ${SHELL_NAME} : ${LOG_INFO}----------------"
    echo "$CTIME ${SHELL_NAME} : ${LOG_INFO}" >> ${SHELL_LOG}
}

# Check Install requirement
install_init(){
    shell_log "=====Begin: Init======"
    mkdir -p ${INSTALL_PATH}/{ollama-volume,openclaw-volume}
    chown -R 1000:1000 ${INSTALL_PATH}/{ollama-volume,openclaw-volume}
}

ollama_install(){
    shell_log "=====Ollama: Start Ollama======"
    docker run -d --restart=always --name opsany-base-ollama \
    -p 8021:11434 -v ${INSTALL_PATH}/ollama-volume:/root/.ollama \
    docker.m.daocloud.io/ollama/ollama:0.18.2
}

openclaw_install(){
    shell_log "=====OpenClaw: Start OpenClaw======"
    docker run -d --restart=always --name openclaw-gateway \
    -p 8022:18789 \
    -v ${INSTALL_PATH}/openclaw-volume:/home/node \
    opsany/openclaw:2026.3.13 "node  dist/index.js gateway --bind lan --port 18789"
}

opsai_uninstall(){
    shell_log "=====Uninstall======"
    docker stop opsany-ollama
    docker rm opsany-ollama
    rm -rf ${INSTALL_PATH}/{ollama-volume}
}

# Main
main(){
    case "$1" in
    install)
        install_init
        ollama_install
        ;;
    uninstall)
        zabbix_uninstall
        ;;
        help|*)
                echo $"Usage: $0 {install|uninstall|help}"
                ;;
esac
}

main $1
