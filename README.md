# 火山引擎刊例价与云迁移报价 Skills

> 一个自包含的 Claude 技能包,用于:(1) **自动同步火山引擎全量产品刊例价**,(2) **根据友商云清单或客户需求生成火山引擎对标报价 Excel**。

[English](#english) · 中文

---

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
                             │ (1) Playwright 自动抓取
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

### 在 Claude Code 中

1. 把整个 `Skills/` 文件夹放到任何工作目录(推荐根目录或 `~/skills/`)。
2. 跟 Claude 说:
   - "更新一下火山引擎所有产品的刊例价" → 触发 Skill 1
   - "把这份阿里云清单做火山报价" → 触发 Skill 2
   - "客户要 N 台 4C16G ECS,给个火山报价单" → Skill 2 模式 2

Claude 会自动识别 SKILL.md 头部的 description 并调用。

### 在其他 Agent 框架中

每个 SKILL.md 末尾标注了"Claude Code 环境对应的工具名"。要移植到别的 agent 运行时,把这些工具名换成等价能力即可:
- `TodoWrite` → 你的任务清单/进度追踪能力
- `AskUserQuestion` → 向用户提单选确认问题的能力
- `mcp__plugin_ecc_playwright__browser_*` → 浏览器自动化(支持导航/evaluate/下载)
- `Read` / `Write` / `Edit` → 文件读写能力

主流程文档全部用"能力描述"而非工具名,所以移植成本很低。

### 验收脚本(必跑)

两个 skill 都带验收脚本,生成后必跑、0 errors 才算完成:

```bash
# 刊例价目录验收
python3 Skills/更新火山引擎产品刊例价/scripts/verify_pricing.py

# 报价 Excel 验收
python3 Skills/云迁移对标报价/scripts/verify_quote.py <报价.xlsx> --strategy A|B|C --scenario 1|2
```

检查项覆盖:派生列是否为公式、合计行 SUM 范围、sheet 数量与策略匹配、品牌分区配色、CSV 同产品多份、空文件、新鲜度等。

## 设计要点

1. **自包含**:整个 `Skills/` 移到任何机器、任何 agent 都能跑,不依赖外部目录。
2. **能力描述化**:工具名不硬编码,移植到非 Claude Code 环境只需把 4~5 类能力替换。
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

## License

MIT(默认选择,需要其他协议请提 issue)。

---

<a name="english"></a>

# Volcengine Pricing & Cloud Migration Quoting Skills

> Self-contained Claude skill bundle for: (1) **auto-syncing the full Volcengine product price list**, and (2) **generating Volcengine quote spreadsheets from competitor cloud inventories or direct customer requirements**.

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
                             │ (1) Playwright scrape
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

### In Claude Code

1. Drop the entire `Skills/` folder anywhere (recommended: workspace root or `~/skills/`).
2. Ask Claude:
   - "Refresh all Volcengine product prices" → triggers Skill 1
   - "Generate a Volcengine quote from this Aliyun inventory" → triggers Skill 2
   - "Customer wants N × 4C16G ECS, give me a quote" → Skill 2 Mode 2

Claude reads each SKILL.md header description and invokes automatically.

### In Other Agent Runtimes

Each SKILL.md ends with a footnote mapping "Claude Code tool names" to capabilities. To port:
- `TodoWrite` → your task-tracking capability
- `AskUserQuestion` → ability to ask a single-choice confirmation
- `mcp__plugin_ecc_playwright__browser_*` → browser automation (navigate / evaluate / download)
- `Read` / `Write` / `Edit` → file I/O

Main flow documents use capability descriptions, not tool names, so porting is cheap.

### Verification Scripts (Mandatory)

Both skills ship verification scripts; must pass with 0 errors before considering output done:

```bash
# Pricing directory verify
python3 Skills/更新火山引擎产品刊例价/scripts/verify_pricing.py

# Quote Excel verify
python3 Skills/云迁移对标报价/scripts/verify_quote.py <quote.xlsx> --strategy A|B|C --scenario 1|2
```

Checks include: derived columns are formulas, total-row SUM ranges, sheet count vs strategy, brand palette applied, duplicate CSVs, empty files, freshness, etc.

## Design Principles

1. **Self-contained** — move `Skills/` to any machine, any agent; no external paths.
2. **Capability-described, not tool-bound** — porting requires swapping ~5 capability names, no rewrite.
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

## License

MIT (safe default — open an issue if you'd prefer another).
