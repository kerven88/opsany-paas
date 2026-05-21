# PaaSAgent 开发指南

## 服务说明

PaaSAgent是Go语言实现的应用引擎Agent，部署在应用服务器上，负责接收AppEngine的指令执行SaaS应用的部署和下架操作。

- **Agent端口**: 4245
- **Nginx端口**: 8085
- **Go**: 1.x

## 目录结构

```
paasagent/
├── core/              # 核心逻辑
├── etc/               # 配置
│   └── build/packages/
│       └── requirements.txt  # Python依赖
├── job/               # 任务处理
├── server/            # HTTP服务
├── vendor/            # 依赖包
├── main.go            # 入口
├── Gopkg.toml        # 依赖管理
├── Makefile          # 构建
└── VERSION          # 版本
```

## 技术栈

- Web框架: labstack/echo
- Python运行时: virtualenv, uwsgi
- 依赖管理: Gopkg (dep)

## 配置

配置文件: `etc/conf/{env}.yaml`

## 构建

```bash
cd paas-ce/paasagent
make build
```

## 运行

```bash
./paasagent -c etc/conf/prod.yaml
```

## 与AppEngine通信

- AppEngine通过HTTP调用Agent接口
- Agent执行部署任务后回写日志到AppEngine