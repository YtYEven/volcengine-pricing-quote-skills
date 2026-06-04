# 火山引擎刊例价与云迁移报价 Skills

> 一个**通用 Agent 技能包**(自包含),用于:(1) **自动同步火山引擎全量产品刊例价**,(2) **根据友商云清单或客户需求生成火山引擎对标报价 Excel**。

[English](#english) · 中文

---

## 适用的 Agent

技能包用"能力描述"而非具体工具名编写,任何满足下文"前置能力"的 Agent 框架都能跑。已验证或预期兼容:

| Agent | 状态 | 备注 |
| --- | --- | --- |
| **Claude Code** (Anthropic) | ✅ 已验证 | 原生开发环境,所有功能开箱即用 |
| **Codex** (OpenAI) | 🟢 兼容 | 需配 Playwright MCP + Python 环境;能力命名替换见下文 |
| **Trae** (字节跳动 IDE) | 🟢 兼容 | 需 IDE 内置浏览器/终端能力 + Python |
| **OpenClaw** | 🟢 兼容 | REPL 模式下需手动确认替代 AskUserQuestion 类交互 |
| **Cursor / Continue / Cline** | 🟢 兼容 | 需 MCP Playwright 或同等浏览器自动化 |
| **自定义 Agent (LangChain / AutoGen 等)** | 🟢 兼容 | 工具链全配齐即可 |

主流程文档(SKILL.md / sheet_strategies.md / pricing_lookup.md 等)用"建立任务清单""向用户提单选确认问题""浏览器导航"这类**能力描述**,每个 SKILL.md 末尾附"Claude Code 工具名对照表"作过渡参考。

## 前置能力(必须)

| 能力 | 哪个 skill 用 | 等价工具示例 |
| --- | --- | --- |
| **文件读/写/编辑** | 两个都用 | Claude Code `Read`/`Write`/`Edit`;Codex 文件工具;Trae IDE 文件 API |
| **Shell / Bash 执行** | 两个都用 | `Bash` 工具(用于 ls/mv/rm/python 跑 verify 脚本) |
| **Python 3 环境** | 报价 skill + 验收脚本 | 系统 python3 + `openpyxl` 包 |
| **浏览器自动化**(导航/JS evaluate/触发下载) | 仅刊例价 skill | Playwright MCP / Puppeteer / 等同能力 |
| **任务清单 / 进度追踪** | 推荐 | Claude Code `TodoWrite`;Codex todo;或退化到 markdown 手记 |
| **单选确认交互** | 报价 skill 推荐 | Claude Code `AskUserQuestion`;退化:直接问用户回答 |

**最低可跑要求**:文件读写 + Bash + Python 3 + openpyxl(可单独跑报价 skill,但需要手动从官网下载 CSV 喂给 `Skills/火山产品刊例价/`)。完整流程额外需要浏览器自动化。

## 包含什么

```
Skills/
├── 更新火山引擎产品刊例价/   # Skill 1:抓取并同步官网刊例价 CSV
│   ├── SKILL.md
│   ├── product_catalog.md      # 74 个产品的代号 + 处理路径(download/snapshot)
│   ├── refresh-catalog.md      # 何时/如何重建 catalog
│   ├── troubleshooting.md      # 10 个已知坑 + 修复方法
│   └── scripts/verify_pricing.py
│
├── 云迁移对标报价/            # Skill 2:生成对标报价 Excel
│   ├── SKILL.md
│   ├── product_mapping.md      # 阿里/腾讯/AWS → 火山 80+ 条映射,带等价度
│   ├── spec_mapping_rules.md   # ECS/RDS/中间件规格映射 + 缺规格经验默认值
│   ├── pricing_lookup.md       # 从本地 CSV 取价的统一规则
│   ├── sheet_strategies.md     # 三种 sheet 分组策略 A/B/C + 自动推荐
│   ├── excel_template.md       # 字段顺序、公式、合计、品牌分区配色
│   └── scripts/verify_quote.py
│
├── 火山产品刊例价/            # 数据源:Skill 1 写入 / Skill 2 读取的 74 份 CSV
│   └── *.csv (74 个,每个产品一份)
│
└── 火山云服务器/              # ECS 选型参考文档
    ├── 实例命名及选型推荐.md
    └── 实例类型和规格.md
```

## 两个 Skill 怎么协作

```
                ┌─────────────────────────────────┐
                │  火山引擎官网 pricing 页面       │
                └────────────┬────────────────────┘
                             │ (1) 浏览器自动化抓取
                             ▼
         ┌──────────────────────────────────────┐
         │  Skill 1: 更新火山引擎产品刊例价      │
         │  (有"价格下载"按钮 → 直接下载         │
         │   无按钮 → 页面快照 + 提取表格)       │
         └────────────┬─────────────────────────┘
                      │ (2) 写入本地 CSV
                      ▼
         ┌──────────────────────────────────────┐
         │  火山产品刊例价/*.csv (74 份)         │
         └────────────┬─────────────────────────┘
                      │ (3) 读取
                      ▼
         ┌──────────────────────────────────────┐
         │  Skill 2: 云迁移对标报价              │
         │  友商清单 → 产品对标 → 规格映射       │
         │   → 取价 → 多 sheet Excel              │
         └────────────┬─────────────────────────┘
                      │ (4) 输出
                      ▼
              <客户名>-火山引擎报价-YYYYMMDD.xlsx
```

## 怎么用

### 1. 拉到本地

```bash
git clone https://github.com/YtYEven/volcengine-pricing-quote-skills.git
# 或把整个 Skills/ 目录拷到你的工作区任何位置
```

### 2. 装依赖

```bash
pip3 install openpyxl
# 浏览器自动化(只在跑 Skill 1 时需要):
# Claude Code: 启用 mcp__plugin_ecc_playwright
# 其他 agent: 装 playwright-mcp 或对应等价 MCP
```

### 3. 跟你的 Agent 说

| 你的需求 | 说什么 | 触发 |
| --- | --- | --- |
| 拉取最新刊例价 | "更新一下火山引擎所有产品的刊例价" | Skill 1(全量) |
| 只更新指定产品 | "更新 ECS、RDS MySQL 的刊例价" | Skill 1(指定) |
| 阿里清单转报价 | "把这份阿里云清单做火山报价" | Skill 2(场景 1) |
| 客户直接报需求 | "客户要 N 台 4C16G ECS,给个报价" | Skill 2(场景 2) |

Agent 会读 `Skills/*/SKILL.md` 顶部 description 自动匹配。如果你的 agent 不会自动发现 skill,把对应 SKILL.md 内容贴进 prompt 即可。

### 4. 跨 Agent 移植速查

如果工具命名不同,SKILL.md 里所有"能力描述"对应的 Claude Code 工具如下,换其他 agent 时替换为等价工具:

| 能力描述(SKILL.md 用语) | Claude Code | 其他 agent 换什么 |
| --- | --- | --- |
| "建立任务清单" | `TodoWrite` | Codex todo / Trae task list / 自定义 |
| "向用户提单选确认问题" | `AskUserQuestion` | 普通对话 + 让用户回答 |
| "浏览器导航" / "页面 evaluate" / "关闭浏览器" | `mcp__plugin_ecc_playwright__browser_*` | playwright-mcp / puppeteer-mcp / 自建 |
| "文件读取能力" | `Read` | 对应 file read 工具 |
| "Excel 写入库" | Python `openpyxl` | 同(无 agent 依赖) |

### 5. 验收脚本(强制)

两个 skill 都带验收脚本,生成后必跑、0 errors 才算完成:

```bash
# 刊例价目录验收
python3 Skills/更新火山引擎产品刊例价/scripts/verify_pricing.py

# 报价 Excel 验收
python3 Skills/云迁移对标报价/scripts/verify_quote.py <报价.xlsx> --strategy A|B|C --scenario 1|2
```

检查项覆盖:派生列是否为公式、合计行 SUM 范围、sheet 数量与策略匹配、品牌分区配色、CSV 同产品多份、空文件、新鲜度等。**这两个脚本不依赖任何 agent**,纯 Python,任何环境都能跑。

## 设计要点

1. **Agent 无关**:所有主流程用能力描述,不绑死工具名。
2. **自包含**:整个 `Skills/` 移到任何机器、任何 agent 都能跑,不依赖外部目录。
3. **正交三层**:
   - Sheet 分组策略 (A/B/C) — 决定有几个 sheet
   - 字段集 (4 种) — 决定每 sheet 列怎么排
   - 品牌分区配色 (1 套) — 决定列怎么涂(基于列名分类,不基于位置)
4. **可追溯**:Excel 所有派生数都是公式(`=单价*数量`),客户点 cell 能看到来源。
5. **缺规格不黑盒**:任何假设都在 Excel 备注列 + "假设与说明" sheet 双重声明。
6. **无对标不硬塞**:写"待补"+ 2~3 个候选,让客户决定。
7. **自动验收**:两个 verify 脚本拦机械错误(公式被改成死值、合计 SUM 范围错位、sheet 数与策略不符)。

## 维护

- **刊例价过时**:本地 CSV mtime > 30 天 → Skill 2 启动前会自动提示先跑 Skill 1。
- **新产品上线**:Skill 1 全量更新过程中若 ≥ 3 个产品代号回落到 ECS 页面 → 自动暂停 + 触发 `refresh-catalog.md` 重建产品目录。
- **新友商产品**:Skill 2 现场对标后,append 一行到 `product_mapping.md`,下次复用。
- **改字段顺序**:改 `excel_template.md` + `verify_quote.py` 同步,品牌配色靠列名自动适配,无需改色。

## 不在 scope 内

- 不实际下单/调用火山引擎采购 API(只产生报价 Excel)。
- 不计算"折扣价/优惠价"(只用官网刊例价 + 包1年/12 月折算)。
- 不评估业务架构是否适合迁移(架构咨询是另一回事)。
- 不抓阿里/腾讯/AWS 官网的当前刊例价(友商价不进报价单,只列产品+规格做溯源)。

## License

MIT(默认选择,需要其他协议请提 issue)。

---

<a name="english"></a>

# Volcengine Pricing & Cloud Migration Quoting Skills

> A **universal agent skill bundle** (self-contained) for: (1) **auto-syncing the full Volcengine product price list**, and (2) **generating Volcengine quote spreadsheets from competitor cloud inventories or direct customer requirements**.

## Supported Agents

The skill pack is written using **capability descriptions** rather than tool names, so any agent framework meeting the prerequisites below can run it. Verified or expected compatible:

| Agent | Status | Notes |
| --- | --- | --- |
| **Claude Code** (Anthropic) | ✅ Verified | Native dev environment; works out of the box |
| **Codex** (OpenAI) | 🟢 Compatible | Needs Playwright MCP + Python; see capability mapping below |
| **Trae** (ByteDance IDE) | 🟢 Compatible | Needs IDE browser/terminal + Python |
| **OpenClaw** | 🟢 Compatible | In REPL mode, replace `AskUserQuestion`-style interactions with direct chat |
| **Cursor / Continue / Cline** | 🟢 Compatible | Needs MCP Playwright or equivalent browser automation |
| **Custom Agents (LangChain / AutoGen / etc.)** | 🟢 Compatible | As long as the toolchain is present |

Main flow documents (SKILL.md / sheet_strategies.md / pricing_lookup.md, etc.) use phrases like *"create task list"*, *"ask user a single-choice confirmation"*, *"browser navigate"* — i.e. **capability descriptions**. Each SKILL.md ends with a footnote mapping these to Claude Code tool names as a porting reference.

## Prerequisites

| Capability | Used by | Equivalent tools |
| --- | --- | --- |
| **File read / write / edit** | Both skills | Claude Code `Read`/`Write`/`Edit`; Codex file tools; Trae IDE file API |
| **Shell / Bash execution** | Both skills | `Bash` tool (for ls/mv/rm and running verify scripts) |
| **Python 3 environment** | Quote skill + verify scripts | System python3 + `openpyxl` package |
| **Browser automation** (navigate / page evaluate / download) | Only pricing skill | Playwright MCP / Puppeteer / equivalent |
| **Task tracking** | Recommended | Claude Code `TodoWrite`; Codex todo; or fallback to markdown notes |
| **Single-choice confirmation** | Quote skill recommended | Claude Code `AskUserQuestion`; fallback: ask user directly |

**Minimum viable setup**: file I/O + Bash + Python 3 + openpyxl (you can run the quote skill standalone but must manually download CSVs into `Skills/火山产品刊例价/`). Full pipeline additionally needs browser automation.

## What's Included

```
Skills/
├── 更新火山引擎产品刊例价/   # Skill 1: scrape & sync official price list CSVs
│   ├── SKILL.md
│   ├── product_catalog.md      # 74 product codes + handling path (download/snapshot)
│   ├── refresh-catalog.md      # when/how to rebuild the catalog
│   ├── troubleshooting.md      # 10 known pitfalls + fixes
│   └── scripts/verify_pricing.py
│
├── 云迁移对标报价/            # Skill 2: generate the quote Excel
│   ├── SKILL.md
│   ├── product_mapping.md      # Aliyun/Tencent/AWS → Volcengine, 80+ entries with equivalence tier
│   ├── spec_mapping_rules.md   # ECS/RDS/middleware spec mapping + defaults for missing specs
│   ├── pricing_lookup.md       # unified rule to fetch prices from local CSVs
│   ├── sheet_strategies.md     # three sheet-grouping strategies A/B/C with auto-recommend
│   ├── excel_template.md       # field order, formulas, totals, brand-zone palette
│   └── scripts/verify_quote.py
│
├── 火山产品刊例价/            # Data source: 74 CSVs (written by Skill 1, read by Skill 2)
│   └── *.csv
│
└── 火山云服务器/              # ECS selection reference docs
    ├── 实例命名及选型推荐.md
    └── 实例类型和规格.md
```

## How the Two Skills Cooperate

```
                ┌─────────────────────────────────┐
                │ Volcengine pricing pages         │
                └────────────┬────────────────────┘
                             │ (1) browser automation
                             ▼
         ┌──────────────────────────────────────┐
         │  Skill 1: Update Volcengine Price    │
         │  (has download button → direct CSV   │
         │   no button → page snapshot extract) │
         └────────────┬─────────────────────────┘
                      │ (2) write
                      ▼
         ┌──────────────────────────────────────┐
         │  火山产品刊例价/*.csv (74 files)      │
         └────────────┬─────────────────────────┘
                      │ (3) read
                      ▼
         ┌──────────────────────────────────────┐
         │  Skill 2: Cloud Migration Quote      │
         │  inventory → product map → spec map  │
         │   → price lookup → multi-sheet xlsx  │
         └────────────┬─────────────────────────┘
                      │ (4) output
                      ▼
              <customer>-volcengine-quote-YYYYMMDD.xlsx
```

## Usage

### 1. Clone

```bash
git clone https://github.com/YtYEven/volcengine-pricing-quote-skills.git
# Or copy the entire Skills/ directory into your workspace.
```

### 2. Install Dependencies

```bash
pip3 install openpyxl
# Browser automation (only needed for Skill 1):
# Claude Code: enable mcp__plugin_ecc_playwright
# Other agents: install playwright-mcp or equivalent MCP
```

### 3. Ask Your Agent

| What you want | Say something like | Triggers |
| --- | --- | --- |
| Refresh prices | "Update all Volcengine product prices" | Skill 1 (full) |
| Update specific products | "Update prices for ECS and RDS MySQL" | Skill 1 (targeted) |
| Aliyun inventory → quote | "Generate a Volcengine quote from this Aliyun inventory" | Skill 2 (scenario 1) |
| Customer direct requirement | "Customer wants N × 4C16G ECS, give me a quote" | Skill 2 (scenario 2) |

Agents read the `Skills/*/SKILL.md` description header to auto-match. If your agent doesn't auto-discover skills, paste the relevant SKILL.md into your prompt.

### 4. Cross-Agent Porting Cheatsheet

If your agent's tool names differ, here's the Claude Code mapping for every capability phrase used in SKILL.md:

| Capability (as used in SKILL.md) | Claude Code | Replace with on other agents |
| --- | --- | --- |
| "create task list" | `TodoWrite` | Codex todo / Trae task list / custom |
| "ask user a single-choice confirmation" | `AskUserQuestion` | plain chat + wait for reply |
| "browser navigate" / "page evaluate" / "close browser" | `mcp__plugin_ecc_playwright__browser_*` | playwright-mcp / puppeteer-mcp / DIY |
| "file read capability" | `Read` | corresponding file-read tool |
| "Excel write library" | Python `openpyxl` | same (no agent dependency) |

### 5. Verification Scripts (Mandatory)

Both skills ship verification scripts; must pass with 0 errors before considering output done:

```bash
# Pricing directory verify
python3 Skills/更新火山引擎产品刊例价/scripts/verify_pricing.py

# Quote Excel verify
python3 Skills/云迁移对标报价/scripts/verify_quote.py <quote.xlsx> --strategy A|B|C --scenario 1|2
```

Checks include: derived columns are formulas, total-row SUM ranges, sheet count vs strategy, brand palette applied, duplicate CSVs, empty files, freshness, etc. **These scripts are pure Python and have zero agent dependency** — they run anywhere.

## Design Principles

1. **Agent-agnostic** — main flow uses capability descriptions, not specific tool names.
2. **Self-contained** — move `Skills/` to any machine, any agent; no external paths.
3. **Orthogonal three-layer system**:
   - Sheet strategy (A/B/C) — how many sheets and what goes where
   - Field set (4 types) — column order per sheet
   - Brand palette (1 set) — column coloring (driven by column name, not position)
4. **Traceable** — every derived value in Excel is a formula (`=unit_price*qty`); click any cell to see provenance.
5. **No black-box defaults** — missing specs surface as explicit assumptions in remarks column + assumption sheet.
6. **No forced mapping** — products without a Volcengine equivalent get "TBD" + 2~3 candidate notes.
7. **Auto-verify** — two verify scripts catch mechanical errors (formula overwritten to literal, wrong SUM range, sheet count mismatch).

## Maintenance

- **Stale prices** — if local CSV mtime > 30 days, Skill 2 prompts to run Skill 1 first.
- **New products** — Skill 1 detects ≥3 product codes falling back to ECS page → auto-pauses and triggers `refresh-catalog.md` to rebuild.
- **New competitor products** — Skill 2 appends a row to `product_mapping.md` after on-the-fly mapping.
- **Field reorder** — change `excel_template.md` and `verify_quote.py` in sync; brand palette adapts automatically by column name.

## Out of Scope

- Does NOT actually place orders / call Volcengine procurement APIs (output is a quote Excel only).
- Does NOT compute discounted prices (uses official list prices + 1-year/12 monthly amortization).
- Does NOT evaluate whether your architecture should migrate (architecture consulting is separate).
- Does NOT scrape competitor (Aliyun/Tencent/AWS) live prices — those don't enter the quote; only product + spec are listed for traceability.

## License

MIT (safe default — open an issue if you'd prefer another).
