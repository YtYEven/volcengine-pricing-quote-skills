# 火山引擎产品目录与处理方式

> 这张表是 SKILL.md 的伴随参考。"方式"列指示该产品默认走哪条路径：
> - `download` — 页面有"价格下载"按钮，点击即可拿到 CSV。
> - `snapshot` — 页面无下载按钮或下载无效,必须通过**浏览器 evaluate 能力**抓 `main.innerText`。
>
> 产品代号即定价 URL `?product=` 参数。

## download（62 个）

| 中文名 | 代号 |
| --- | --- |
| 云服务器 | ECS |
| 弹性块存储 | EBS |
| 公网IP | EIP |
| 共享带宽包 | BWP |
| NAT网关 | NAT |
| 负载均衡 | CLB |
| 应用型负载均衡 | ALB |
| 网络型负载均衡 | NLB |
| VPN连接 | VPN |
| 专线连接 | DirectConnect |
| 云企业网 | CEN |
| 对象存储 | TOS |
| 文件存储 NAS | NAS |
| 文件存储 vePFS | vePFS |
| 大数据文件存储 | CFS |
| 镜像仓库 | CR |
| 云数据库 MySQL 版 | RDS-MySQL |
| 云数据库 PostgreSQL 版 | RDS-PostgreSQL |
| 云数据库 veDB MySQL 版 | veDB-MySQL |
| 云数据库RDS SQL Server 版 | RDS-SQLServer |
| 文档数据库 MongoDB 版 | MongoDB |
| 表格数据库 HBase 版 | HBase |
| 缓存数据库 Redis 版 | Redis |
| 数据库传输服务 | DTS |
| 数据库工作台 | DBW |
| 数据闪送服务 | DTSv2 |
| 消息队列 Kafka版 | Kafka |
| 消息队列 RabbitMQ版 | RabbitMQ |
| 消息队列 RocketMQ版 | RocketMQ |
| 云搜索服务 | ESCloud |
| 云监控 | VMS |
| 日志服务 | TLS |
| 函数服务-事件函数 | VeFaaS |
| 机器学习平台 | ML-Platform |
| 火山方舟 | Ark |
| 扣子 | Coze |
| 语音技术 | Speech |
| 增长分析 | DataFinder |
| 增长营销平台-SaaS | GMP |
| 视频点播 | VOD |
| 视频直播 | LIVE |
| 慢直播 | SlowLive |
| 内容分发网络 | CDN |
| 全站加速 | DCDN |
| 边缘计算节点 | EdgeNode |
| 边缘渲染农场 | EdgeRender |
| TrafficRoute DNS套件 | TrafficRoute |
| 域名注册 | Domain |
| SSL证书 | SSL |
| Web应用防火墙 | WAF |
| DDoS高防 | AntiDDoS |
| 云防火墙 | CFW |
| 云安全中心 | CSC |
| 高级网络威胁检测系统 | ANTS |
| 国内短信 | SMS |
| 云游戏 | veGame |
| E-MapReduce | EMR |
| AI 数据湖服务 | LAS |
| 大数据研发治理套件 | DataLeap |
| 流式计算 Flink版 | Flink |
| 向量数据库 Milvus 版 | Milvus |
| 生信操作系统-云平台版 | BioOS |

## snapshot（12 个）

| 中文名 | 代号 | 备注 |
| --- | --- | --- |
| 中转路由器 | TransitRouter | |
| 私网连接网关 | PrivateLinkGateway | |
| 流量镜像 | traffic_mirror | |
| DDoS原生防护 | AntiDDoS-origin | |
| 云原生消息引擎 | BMQ | 含 BMQ + MQTT 两段表 |
| 向量数据库 | VikingDB | |
| 实时音视频 | veRTC | 按钮存在但点击无下载，必须 snapshot |
| 容器服务-托管版 | VKE | |
| 弹性文件存储 | EFS | |
| 托管Prometheus | VMP | |
| ByteHouse-云数仓版-SaaS | bytehouse | 注意是小写 |
| ByteHouse企业版 | bytehouse_enterprise | |

## 用户给中文名时的模糊匹配

允许下列等价：
- "RDS / MySQL" → 云数据库 MySQL 版
- "ECS / 云主机" → 云服务器
- "OSS" → 对象存储（TOS）
- "CDN" → 内容分发网络
- "Kafka" → 消息队列 Kafka版
- "ByteHouse" 不带后缀时，提示用户选 SaaS 还是 企业版
