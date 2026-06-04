# 友商产品 → 火山引擎产品对照表

> 用于云迁移对标报价。已知映射在此表中查；不在此表中的产品按"现场对标流程"章节处理。
> 表格按"完全等价 / 功能基本等价 / 非完全等价"三档标记，最后一档需要在 Excel 备注列写说明。

## 阿里云 → 火山引擎

| 阿里云产品 | 火山引擎对标 | 等价度 | 备注 |
| --- | --- | --- | --- |
| 云服务器 ECS | 云服务器 | 完全 | |
| 块存储 / ESSD 云盘 | 弹性块存储 | 完全 | ESSD PL0 ↔ 极速型 SSD PL0；ESSD AutoPL ↔ FlexPL |
| 弹性公网IP | 公网IP | 完全 | |
| 共享带宽 | 共享带宽包 | 完全 | |
| NAT网关 | NAT网关 | 完全 | |
| 传统型负载均衡 CLB | 负载均衡 | 完全 | 阿里 CLB(四层) → 火山 CLB |
| 应用型负载均衡 ALB | 应用型负载均衡 | 完全 | |
| 网络型负载均衡 NLB | 网络型负载均衡 | 完全 | |
| VPN 网关 | VPN连接 | 完全 | |
| 高速通道（专线） | 专线连接 | 完全 | |
| 云企业网 CEN | 云企业网 | 完全 | |
| 对象存储 OSS | 对象存储 TOS | 完全 | |
| 文件存储 NAS | 文件存储 NAS | 完全 | 性能型/容量型对齐 |
| CPFS | 文件存储 vePFS | 基本等价 | |
| 容器镜像服务 ACR | 镜像仓库 CR | 完全 | |
| 容器服务 Kubernetes 版 ACK | 容器服务-托管版 VKE | 完全 | 管理面 + 工作节点要分别计价 |
| 云数据库 RDS MySQL | 云数据库 MySQL 版 | 完全 | |
| 云数据库 RDS PostgreSQL | 云数据库 PostgreSQL 版 | 完全 | |
| 云数据库 RDS SQL Server | 云数据库 RDS SQL Server 版 | 完全 | |
| 云数据库 PolarDB MySQL | 云数据库 veDB MySQL 版 | 基本等价 | |
| 云数据库 MongoDB 版 | 文档数据库 MongoDB 版 | 完全 | |
| 云数据库 HBase | 表格数据库 HBase 版 | 完全 | |
| 云数据库 Redis(开源版) | 缓存数据库 Redis 版 | 完全 | 分片 vs 非分片单价不同 |
| 云数据库 Tair(企业版/持久内存型) | 缓存数据库 Redis 版 | 非完全等价 | Tair 专属能力(TairString/TairHash/持久内存等)无对应,按 Redis 标准版降级,备注差异 |
| 数据传输服务 DTS | 数据库传输服务 | 完全 | |
| 数据库自治服务 DAS | 数据库工作台 DBW | 基本等价 | |
| 云消息队列 Kafka | 消息队列 Kafka版 | 完全 | |
| 云消息队列 RabbitMQ | 消息队列 RabbitMQ版 | 完全 | |
| 云消息队列 RocketMQ | 消息队列 RocketMQ版 | 完全 | Serverless 系列火山暂用 RocketMQ 实例版替代 |
| 云消息队列 MQTT | 云原生消息引擎 BMQ (MQTT) | 完全 | |
| 检索分析服务 Elasticsearch | 云搜索服务 ESCloud | 完全 | |
| 云监控（Pro） | 云监控 | 完全 | |
| 可观测可视化 Grafana 版 | 托管 Prometheus VMP + 自建/外接 Grafana | 非完全等价 | 火山侧无独立托管 Grafana 产品;VMP 是 Prometheus 引擎,Grafana 看板需自建或外接 |
| 日志服务 SLS | 日志服务 TLS | 完全 | 写入/索引/存储分别计价 |
| 应用实时监控服务 ARMS | 应用性能监控全链路版 | 非完全等价 | 功能覆盖不完全一致，需个案对比 |
| 函数计算 FC | 函数服务 VeFaaS | 完全 | |
| 内容分发网络 CDN | 内容分发网络 CDN | 完全 | |
| 全站加速 DCDN / 边缘安全加速 | 全站加速 | 完全 | |
| 边缘节点服务 ENS | 边缘计算节点 | 完全 | |
| 视频点播 VOD | 视频点播 | 完全 | |
| 视频直播 | 视频直播 | 完全 | |
| 音视频通信 RTC | 实时音视频 veRTC | 完全 | |
| 云解析 DNS | TrafficRoute DNS套件 | 完全 | |
| 云解析 PrivateZone | TrafficRoute DNS套件 (内网解析) | 完全 | |
| 域名服务 | 域名注册 | 完全 | |
| 数字证书管理（原 SSL证书） | SSL证书 | 完全 | |
| Web应用防火墙 | Web应用防火墙 | 完全 | |
| 云防火墙 | 云防火墙 | 完全 | |
| DDoS 防护 / DDoS 高防 | DDoS高防 | 完全 | 弹性按峰值 |
| DDoS 原生防护 | DDoS原生防护 | 完全 | |
| 云安全中心 | 云安全中心 | 完全 | |
| 短信服务 | 国内短信 | 完全 | |
| 阿里云 PAI | 机器学习平台 | 基本等价 | |
| 通义千问/百炼大模型 | 火山方舟 | 基本等价 | 都是大模型平台,模型生态/Agents/Guardrails/知识库封装不一致;按 token 计费 |
| 百炼 Coding Plan | 火山方舟 Coding Plan | 完全 | |
| 智能开放搜索 OpenSearch | 云搜索服务 ESCloud | 基本等价 | 火山云搜索已支持全文+向量+混合 AI 搜索;纯向量场景可补 VikingDB |
| 智能语音交互 | 语音技术 | 基本等价 | |
| 视觉智能开放平台(OCR 子能力) | 文字识别 | 完全 | 同 line 67,见拆分 |
| 视觉智能开放平台(图像/视频理解子能力) | 火山方舟多模态能力 | 基本等价 | 阿里此平台覆盖 13 大类视觉能力,需按子能力逐项对标;火山侧无同层级独立产品 |
| 文字识别 OCR | 文字识别 | 完全 | |
| 云数据库 ClickHouse / Hologres | ByteHouse-云数仓版-SaaS | 基本等价 | |
| 云原生大数据计算服务 MaxCompute | ByteHouse-云数仓版-SaaS | 非完全等价 | 架构差异较大，需结合业务场景说明 |
| 实时计算 Flink | 流式计算 Flink版 | 完全 | |
| E-MapReduce EMR | E-MapReduce | 完全 | |
| 智能数据建设与治理 Dataphin | 大数据研发治理套件 | 基本等价 | 两边都覆盖集成/开发/治理/资产,但官方定位和能力封装不一致 |
| DataWorks | 大数据研发治理套件 | 基本等价 | |
| 数据湖构建 DLF(元数据/权限管理) | 大数据研发治理套件(DataLeap 部分) | 基本等价 | DLF 偏湖仓元数据/治理平台,对应火山 DataLeap 子能力 |
| 数据湖分析 DLA(Serverless 查询) | E-MapReduce / AI 数据湖服务 LAS | 基本等价 | DLA 偏 Serverless 查询;LAS 现已偏向多模态 AI 数据湖,需按场景拆分 |
| 向量检索服务 / 阿里云 Lindorm 向量 | 向量数据库 VikingDB | 基本等价 | |
| 云效（DevOps） | 持续交付 | 非完全等价 | |

## 腾讯云 → 火山引擎（常见项）

| 腾讯云产品 | 火山引擎对标 | 等价度 | 备注 |
| --- | --- | --- | --- |
| 云服务器 CVM | 云服务器 | 完全 | |
| 云硬盘 CBS | 弹性块存储 | 完全 | |
| 对象存储 COS | 对象存储 TOS | 完全 | |
| 文件存储 CFS | 文件存储 NAS | 完全 | |
| 云数据库 MySQL/PostgreSQL/SQL Server | 云数据库对应版本 | 完全 | |
| 云数据库 Redis | 缓存数据库 Redis 版 | 完全 | |
| 负载均衡 CLB | 负载均衡 / 应用型 / 网络型 | 完全 | 按 L4/L7 分流 |
| 弹性公网 IP EIP | 公网IP | 完全 | |
| 内容分发网络 CDN | 内容分发网络 | 完全 | |
| TKE 容器服务 | 容器服务-托管版 | 完全 | |
| 消息队列 CKafka | 消息队列 Kafka版 | 完全 | |
| 消息队列 TDMQ for RocketMQ | 消息队列 RocketMQ版 | 完全 | |
| 消息队列 TDMQ for Pulsar | 无直接对标 | —— | 火山侧无 Pulsar 托管,候选:Kafka 版 / RocketMQ 版替代 |
| 消息队列 TDMQ for MQTT | 云原生消息引擎 BMQ (MQTT) | 完全 | |
| Web 应用防火墙 WAF | Web应用防火墙 | 完全 | |
| 大禹 DDoS 防护 | DDoS高防 | 完全 | |
| 实时音视频 TRTC | 实时音视频 veRTC | 完全 | |

## AWS → 火山引擎（常见项）

| AWS 产品 | 火山引擎对标 | 等价度 | 备注 |
| --- | --- | --- | --- |
| EC2 | 云服务器 | 完全 | |
| EBS | 弹性块存储 | 完全 | gp3 → 极速型 SSD FlexPL |
| S3 | 对象存储 TOS | 完全 | |
| EFS | 文件存储 NAS | 完全 | |
| RDS MySQL/PostgreSQL/SQL Server | 云数据库对应版本 | 完全 | |
| ElastiCache for Redis | 缓存数据库 Redis 版 | 完全 | |
| DocumentDB | 文档数据库 MongoDB 版 | 基本等价 | |
| ALB / NLB / CLB | 应用型 / 网络型 / 负载均衡 | 完全 | |
| Elastic IP | 公网IP | 完全 | |
| CloudFront | 内容分发网络 | 完全 | |
| EKS | 容器服务-托管版 | 完全 | |
| ECR | 镜像仓库 | 完全 | |
| MSK (Kafka) | 消息队列 Kafka版 | 完全 | |
| Lambda | 函数服务 VeFaaS | 完全 | |
| SageMaker | 机器学习平台 | 基本等价 | |
| Bedrock | 火山方舟 | 基本等价 | 都是大模型应用构建平台,模型生态/Agents/Guardrails/知识库封装不一致 |
| Route 53 | TrafficRoute DNS套件 | 完全 | |

## 现场对标流程（产品不在以上表里时）

1. 在友商官方产品页找产品定义、计费维度。
2. 在火山引擎 https://www.volcengine.com/products 找类似产品。
3. 对照 3 个维度：**功能** / **架构** / **计费模型**。
4. 决定等价度：完全 / 基本等价 / 非完全等价。
5. 写入 Excel 的"产品对照表" sheet，并把这条对标 **append 到本文件**（让后续报价复用）。
6. 如果找不到对标：在 Excel 行的"火山产品"列写"无直接对标"，备注列给 2~3 个可能的近似产品供客户选。

## 一对多 / 多对一的处理

- **一对多**（一个阿里产品对应多个火山产品）：在对照表 sheet 多列几行，每行一个候选火山产品；让客户在备注列勾选。例：阿里 ECS 在某些重度本地盘场景需要拆成"火山 ECS + 弹性块存储独购"。
- **多对一**（多个阿里产品对应一个火山产品）：合并到一行报价，备注列写明合并依据。例：阿里"弹性公网 IP + 共享带宽"两条 → 火山"公网 IP（含带宽包）"一行。

## 易错点

- **阿里 ECS 突发性能型 t6/u1** 通常不应映射到火山突发型 t2，而是映射到火山共享型 s2 或入门通用 g4i.large，因为火山的 t2 性能模型差异较大。
- **阿里云数据库 Tair 持久内存型** 没有完全等价产品，按 Redis 标准版降级映射并备注差异。
- **阿里云日志服务 SLS 的写入/索引/存储三段计费** 对应火山 TLS 的 0.85/0.35/0.0115 三段单价，必须分项列出，不能合并。
- **MaxCompute** 与 **ByteHouse** 架构差异大（Hadoop 生态 vs 列存数仓），仅在客户场景明确是 BI 报表/即席查询时才推荐对标，做 ETL 重度场景慎重。
