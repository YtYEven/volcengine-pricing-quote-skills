# 规格映射规则

> 把友商规格映射到火山引擎规格的统一规则。所有"经验假设"必须在 Excel 备注列写明。

## 一、ECS（云服务器）

### 1. 三步映射

1. **vCPU / 内存对齐**：vCPU 数和内存 GiB 完全相同。比例不同（如 4C16G vs 4C8G）按客户原比例选火山对应规格族。
2. **代次默认**：客户没说明 → **最新代次 + Intel**（当前 `g4i / c4i / r4i / i4i`）。客户原侧用 AMD/ARM 时同代次走 a/y 后缀（如 g4a / g4y），写在备注。
3. **存储对齐**：系统盘容量 + 数据盘容量分别对齐；磁盘类型见下文。

### 2. 规格族选择

来源：[../火山云服务器/实例命名及选型推荐.md](../火山云服务器/实例命名及选型推荐.md)

| 业务场景 | 推荐规格族（默认 Intel 4 代） | 说明 |
| --- | --- | --- |
| Web/应用服务、中间件、轻量数据库 | g4i（通用型 1:4） | 默认兜底；客户没说工作负载就用 g4i |
| 计算密集、批处理、视频转码、ML 训练 | c4i（计算型 1:2） | |
| MySQL/PG/Oracle/SQL Server、Redis、Kafka | r4i（内存型 1:8） | 数据库/缓存/MQ 强烈推荐 |
| 本地 SSD 数据库、Elasticsearch、HBase | i4i（本地盘型 1:8） | 阿里 i 系列→火山 i 系列 |
| Hadoop、Spark、ClickHouse、对象/日志存储 | d4i（大数据型 1:4，大本地HDD） | 数据规模 ≥ TB 才考虑 |
| 突发型（阿里 t6/u1） | s2 / g4i.large | **不要**映射到火山 t2，性能模型差异大 |

### 3. 常见友商规格 → 火山规格示例

| 阿里规格 | 火山映射 | 备注 |
| --- | --- | --- |
| ecs.g7.large (2C8G) | ecs.g4i.large | |
| ecs.g7.xlarge (4C16G) | ecs.g4i.xlarge | |
| ecs.g7.2xlarge (8C32G) | ecs.g4i.2xlarge | |
| ecs.c7.xlarge (4C8G) | ecs.c4i.xlarge | |
| ecs.r7.xlarge (4C32G) | ecs.r4i.xlarge | |
| ecs.t6-c1m2.large (2C4G 突发) | ecs.g4i.large（共享/突发拉平为通用） | 备注：原突发型，已按通用型估算 |
| ecs.u1-c1m4.xlarge (4C16G) | ecs.g4i.xlarge | |
| ecs.i3.2xlarge (8C64G + 本地 NVMe) | ecs.i4i.2xlarge | 保留本地盘容量 |
| AWS m6i.xlarge (4C16G) | ecs.g4i.xlarge | |
| AWS r6i.xlarge (4C32G) | ecs.r4i.xlarge | |
| AWS c6i.xlarge (4C8G) | ecs.c4i.xlarge | |

### 4. 磁盘映射

| 阿里 / AWS 盘 | 火山映射 | 默认单价 |
| --- | --- | --- |
| ESSD PL0 / gp2 / gp3（中低 IOPS） | 极速型 SSD PL0 | 0.5 元/GiB/月 |
| ESSD PL1 / gp3 高 IOPS | 极速型 SSD FlexPL（基础档） | 1.0 元/GiB/月 |
| ESSD PL2 / io1 / io2 | 极速型 SSD FlexPL（高档） | 1.0 元/GiB/月 + IOPS/吞吐附加，按 CSV 取 |
| ESSD AutoPL | 极速型 SSD FlexPL | 1.0 元/GiB/月 |
| 高效云盘 / 普通云盘 | 高性能型 HDD | 看 CSV |

**默认**：系统盘走 **PL0**（0.5）；数据盘走 **FlexPL**（1.0）。客户原始就是 PL0 → 数据盘也用 PL0。

## 二、RDS / 数据库

### 1. 三步映射

1. **vCPU / 内存对齐**。
2. **存储容量对齐**（不论原侧是 ESSD 还是本地 SSD，火山侧默认 ESSD PL1）。
3. **架构对齐**：高可用版/集群版 → 火山高可用；单机 → 火山单机。**默认双节点高可用**（除非客户写明单机）。

### 2. 常见映射示例

| 阿里 RDS 规格 | 火山映射 |
| --- | --- |
| mysql.n2.medium.1 (1C2G 单机) | rds.mysql.b2.small.1 |
| mysql.n4.medium.2 (2C4G 双节点) | rds.mysql.b2.small.2（高可用） |
| mysql.x4.large.2 (4C16G 双节点) | rds.mysql.b2.large.2 |
| mysql.x8.2xlarge.2 (16C128G 双节点) | rds.mysql.b2.4xlarge.2 |
| polardb.x4.large.2 (4C16G PolarDB) | veDB MySQL 4C16G（备注：架构差异，按 vCPU/内存估） |

### 3. Redis / Kafka / RocketMQ

| 类型 | 映射规则 |
| --- | --- |
| Redis 主备 / 集群 | 内存容量对齐；分片版本和非分片版本单价不同，**优先对齐分片数** |
| Kafka | 对齐 **峰值流量(MB/s) + 存储容量**；分区数差异在备注 |
| RocketMQ | 对齐 **TPS 档位 + 存储**；阿里 Serverless 系列 → 火山实例版（备注） |
| MongoDB | 对齐 **vCPU/内存/存储**；副本集数量对齐 |

## 三、缺规格的经验默认值

客户清单上只写 "ECS x 8 台"、"RDS x 2 台" 这种没规格的，按下表做**模拟假设**，并在备注列写 "**假设：xxx，待客户确认**"。

### ECS

| 客户业务规模线索 | 默认假设 |
| --- | --- |
| 小型业务 / 个人站 / 测试环境 | ecs.g4i.large (2C8G) + 系统盘 PL0 40 GiB |
| 中型业务 / 常规生产 Web | ecs.g4i.xlarge (4C16G) + 系统盘 PL0 50 GiB + 数据盘 FlexPL 100 GiB |
| 大型业务 / 高并发 | ecs.g4i.2xlarge (8C32G) + 系统盘 PL0 50 GiB + 数据盘 FlexPL 200 GiB |
| 数据库专用机 | ecs.r4i.xlarge (4C32G) + 系统盘 PL0 50 GiB + 数据盘 FlexPL 500 GiB |
| 完全无线索 | ecs.g4i.xlarge (4C16G) + 50 GiB PL0（中型兜底） |

### RDS

| 线索 | 默认假设 |
| --- | --- |
| 没写规格 | rds.mysql.b2.large.2（4C16G 高可用）+ 100 GiB |
| 说"小库" | rds.mysql.b2.small.2（2C4G 高可用）+ 50 GiB |
| 说"大库 / 核心库" | rds.mysql.b2.2xlarge.2（8C32G 高可用）+ 500 GiB |

### Redis

- 没写规格 → 4 GiB 主备版（双副本）

### 公网带宽

- 没写规格 → 5 Mbps 按固定带宽（华东2）

## 四、网络/安全/其他

| 产品 | 映射维度 |
| --- | --- |
| 公网 IP | 个数 + 带宽 Mbps（按固定带宽或按流量分别取价） |
| NAT 网关 | 规格档（小型/中型/大型）+ 流量计费 |
| CLB / ALB / NLB | 实例规格 + LCU/连接数 估算 |
| WAF | 套餐版本（标准/高级/企业/旗舰）+ 域名数 + QPS |
| DDoS 高防 | 保底带宽 + 弹性峰值 + 业务带宽 |
| CDN / DCDN | 按月流量阶梯（GB→TB→PB）；缺线索 → 默认 1 TB/月 |
| 对象存储 TOS | 存储容量 + 请求次数 + 公网下行流量；默认只算容量，其他写"按量未计入" |
| TLS 日志 | 写入/索引/存储 三段分别取价（必拆，不能合并） |

## 五、写入备注列的话术模板

- 缺规格：`假设：4C16G + 50G PL0 + 100G FlexPL（中型业务默认），待客户确认。`
- 无对标：`无直接对标，候选：A产品 / B产品 / C产品，请客户确认。`
- 突发型映射：`原阿里 t6/u1 突发型已按火山通用型 g4i 估算（性能模型差异）。`
- 隐藏成本未计：`未计入公网带宽 / 备份存储 / 跨可用区流量。`
- 架构差异：`PolarDB → veDB MySQL，按 vCPU/内存估算，分布式架构差异需个案验证。`
- 阶梯计价：`CDN 按 1 TB/月 假设取第一档单价，超出按阶梯。`
