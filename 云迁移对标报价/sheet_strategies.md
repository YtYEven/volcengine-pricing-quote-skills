# Sheet 策略

> 三种 sheet 分组策略 A/B/C。根据产品数量和类别自动推荐,并通过**向用户提单选确认问题的能力**让用户确认。

## 一、产品分类标签（13 类）

把火山 74 个产品按业务类别归类，决定走哪些 sheet：

| 标签 | 火山产品（示例） |
| --- | --- |
| compute | 云服务器、弹性容器实例、边缘计算节点、GPU 云服务器 |
| db | 云数据库 MySQL / PostgreSQL / RDS SQL Server、veDB MySQL、文档数据库 MongoDB、缓存数据库 Redis、表格数据库 HBase |
| storage | 弹性块存储、对象存储 TOS、文件存储 NAS、文件存储 vePFS、弹性文件存储 EFS |
| network | 公网IP、NAT网关、负载均衡 CLB/ALB/NLB、VPN连接、专线连接、云企业网、中转路由器、私网连接 |
| security | Web应用防火墙、云防火墙、DDoS高防、DDoS原生防护、云安全中心、SSL证书 |
| mq | 消息队列 Kafka/RocketMQ/RabbitMQ、云原生消息引擎 BMQ |
| bigdata | ByteHouse 云数仓/企业版、E-MapReduce、流式计算 Flink版、大数据研发治理套件、AI 数据湖服务 LAS |
| ai | 火山方舟、机器学习平台、向量数据库 VikingDB、文字识别、图像理解、语音技术 |
| video | 视频点播、视频直播、实时音视频 veRTC、内容分发网络 CDN、全站加速 |
| container | 容器服务-托管版 VKE、镜像仓库 CR、函数服务 VeFaaS |
| ops | 云监控、日志服务 TLS、托管Prometheus VMP、应用性能监控、数据库工作台 DBW |
| domain | TrafficRoute DNS套件、域名注册 |
| other | 国内短信、其他 |

## 二、三种策略

### 策略 A：极简（4 sheet）

适用：报价产品 ≤ 10 个，单一业务场景（如纯 Web 业务、纯数据库迁移）。

| Sheet | 内容 |
| --- | --- |
| 产品对照表 | 友商→火山映射全表（场景 1 才有，场景 2 跳过）|
| 包年报价 | 所有包年包月的产品（compute + db + network + storage + security + mq 全混排）|
| 按量计费 | CDN、TLS、对象存储流量、火山方舟 token 等按量项 |
| 假设与说明 | 缺规格假设、无对标、隐藏成本、地域默认 |

**布局优势**：sheet 少，客户一眼能看全。
**风险**：包年 sheet 行多了字段冗余（实例+存储字段和单存储字段挤一起）。

### 策略 B：按结构（6 sheet,**默认**）

适用：11~25 个产品，多种结构混合（既有 ECS+RDS 又有 OSS+WAF）。

| Sheet | 内容 | 字段集 |
| --- | --- | --- |
| 产品对照表 | 全部友商→火山映射（场景1）| —— |
| ECS+RDS 报价 | 实例+存储二元结构（云服务器、各类数据库、Redis、ES 等带实例的产品）| 实例+存储二元字段集 |
| 单存储与流量 | 对象存储、文件存储、CDN 流量、TLS 等 | 单存储字段集 |
| 网络与安全 | 公网IP、NAT、CLB、WAF、DDoS、VPN、专线 | 网络/安全字段集 |
| 按量计费 | 火山方舟、VikingDB、CDN 阶梯、TLS、OSS 流量 | 按量字段集 |
| 假设与说明 | | —— |

**布局优势**：字段不会乱串。客户能按"我要看 ECS / 我要看 OSS"切换。
**风险**：边界品有时不好放（如 Kafka 既算"实例+存储"又有按量出流量），靠备注说明。

### 策略 C：按业务类别（8~12 sheet）

适用：25+ 个产品，或涉及 5+ 个业务大类（含容器、AI、大数据、视频等专项）。

| Sheet | 内容 |
| --- | --- |
| 产品对照表 |  |
| 计算 (compute) | ECS、GPU、边缘节点、容器实例 |
| 数据库 (db) | MySQL/PG/SQL Server/veDB/MongoDB/Redis |
| 存储 (storage) | 块存储、对象存储、文件存储 |
| 网络 (network) | 公网IP、NAT、LB、VPN、专线、CEN |
| 安全 (security) | WAF、DDoS、云防火墙、安全中心 |
| 容器与中间件 (container+mq) | VKE、CR、VeFaaS、Kafka、RocketMQ |
| 大数据 (bigdata) | ByteHouse、EMR、Flink、Dataphin |
| AI (ai) | 火山方舟、ML 平台、VikingDB、OCR |
| 视频与 CDN (video) | VOD、直播、veRTC、CDN、全站加速 |
| 运维 (ops) | 监控、TLS、VMP、APM |
| 按量计费汇总 | 所有按量项交叉引用 |
| 假设与说明 |  |

**布局优势**：客户按产品域看，方便分团队 review。
**风险**：sheet 多，总价汇总需要单独一个汇总 sheet（或在 README sheet 给跨 sheet SUM 公式）。

## 三、自动推荐逻辑

```
N = 报价产品总数（友商清单产品数 / 场景2的需求项数）
M = 涉及的业务大类数（按 13 类去重）

if N <= 10 and M <= 3:
    推荐 A
elif N <= 25 and M <= 5:
    推荐 B  # 默认
else:
    推荐 C
```

边界情况：
- 即使 N 少但客户明说"按业务部门 review" → 走 C。
- 即使 N 多但都是同一类（如 50 台不同规格的 ECS）→ 走 A 也可。

## 四、与用户确认

每次必须通过**向用户提单选确认问题的能力**(Claude Code 中对应 `AskUserQuestion`)跟用户确认。问题模板:

> **header**: Sheet 策略
> **question**: 这次报价涉及 N 个产品 / M 个业务大类,建议用策略 ?,您希望用哪种 sheet 结构?
> **options**:
> 1. 策略 B - 按结构分(推荐):产品对照表 + ECS/DB 实例 + 单存储 + 网络安全 + 按量 + 假设说明(共 6 sheet)
> 2. 策略 A - 极简:产品对照表 + 包年报价 + 按量 + 假设说明(共 4 sheet)
> 3. 策略 C - 按业务类别:按 compute/db/storage/network/security/bigdata/ai/... 分多个 sheet(8~12)
> 4. 跳过对照表(场景 2 非迁移):直接出报价 sheet,不要友商列

用户可选 "Other" 自由输入定制结构（如 "把数据库单独拎出来，其他合并"）。

## 五、场景 2 调整

场景 2（直接需求 → 报价）时：
- 去掉"产品对照表" sheet
- 去掉所有报价 sheet 中的 `阿里产品` `阿里规格` 两列
- 其他字段、合计行、假设说明 sheet 保持

## 六、合计与跨 sheet 汇总

- 每个数据 sheet 底部一行 **合计**：`数量` 列 `=SUM(...)`、`月总价` 列 `=SUM(...)`、`周期总价` 列 `=SUM(...)`。
- 多 sheet 时（B/C）在 "假设与说明" sheet 上方 / 单独 "总览" sheet 给跨 sheet SUM：
  ```
  =SUM(ECS报价!月总价列) + SUM(单存储!月总价列) + ...
  ```
- 按量计费项 **不参与** 包年总价 SUM（注释里写明"按量按用量结算，不入包年总价"）。
