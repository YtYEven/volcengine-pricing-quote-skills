# Excel 模板规范

> 生成 xlsx 的统一字段顺序、公式约定、合计行规范、openpyxl 代码模式。

## 一、字段集

### 1. 实例 + 存储二元（ECS、RDS、Redis、ES 等）

| 列 | 说明 | 来源 |
| --- | --- | --- |
| 阿里产品 | 友商产品名（场景2去掉） | 输入 |
| 阿里规格 | 友商规格（场景2去掉） | 输入 |
| 类别 | compute / db / mq 等 | 自动归类 |
| 火山产品 | 火山产品中文名 | product_mapping |
| 火山规格 | 火山实例规格码（ecs.g4i.xlarge）| spec_mapping |
| 配置说明 | "4C16G + 50G PL0 + 100G FlexPL" | 拼接 |
| 实例月单价 | 元 | CSV 取 |
| 存储月单价 | 元 | 公式：`= 单GB价 * 容量` |
| 单台月价 | 元 | 公式：`= 实例月单价 + 存储月单价` |
| 数量 | 台 | 输入 |
| 月总价 | 元 | 公式：`= 单台月价 * 数量` |
| 计费周期 | 1年/12月/按量 | 默认 1年 |
| 周期总价 | 元 | 公式：`= 月总价 * 周期月数` |
| 地域 | 华东2(上海) | 默认 |
| 备注 | 假设/差异/未计入 | 文本 |

### 2. 单存储（OSS、文件存储、块存储独购）

| 列 |
| --- |
| 阿里产品 / 阿里规格（场景2去掉） / 火山产品 / 存储类型 / 容量(GiB) / 容量单价(元/GiB/月) / 月总价 / 计费周期 / 周期总价 / 地域 / 备注 |

公式：`月总价 = 容量 * 容量单价`

### 3. 网络/安全

| 列 |
| --- |
| 阿里产品 / 阿里规格 / 火山产品 / 规格/套餐 / 月单价 / 数量 / 月总价 / 计费周期 / 周期总价 / 地域 / 备注 |

公式：`月总价 = 月单价 * 数量`

### 4. 按量计费

| 列 |
| --- |
| 阿里产品 / 阿里规格 / 火山产品 / 火山规格 / 计费维度 / 单价 / 单位 / 估算说明 / 地域 / 备注 |

无 SUM 列（按用量结算）。可加 `估算月用量` 和 `估算月总价（参考）` 两列（公式），并明确"参考估算，不入包年总价"。

## 二、合计行

每个数据 sheet 最后一行。**字段顺序与列字母严格对应表 1**：

| # | 列 | Excel 列字母 | 合计行公式 |
| --- | --- | --- | --- |
| 1 | 阿里产品 | A | — |
| 2 | 阿里规格 | B | — |
| 3 | 类别 | C | — |
| 4 | 火山产品 | D | — |
| 5 | 火山规格 | E | — |
| 6 | 配置说明 | F | 写"合计" |
| 7 | 实例月单价 | G | — |
| 8 | 存储月单价 | H | — |
| 9 | 单台月价 | I | — |
| 10 | 数量 | J | `=SUM(J2:J{last})` |
| 11 | 月总价 | K | `=SUM(K2:K{last})` |
| 12 | 计费周期 | L | — |
| 13 | 周期总价 | M | `=SUM(M2:M{last})` |
| 14 | 地域 | N | — |
| 15 | 备注 | O | — |

**场景 2** 模式（去掉 A/B 两列）字段顺序整体左移 2 列，对应公式列变成：数量=H、月总价=I、周期总价=K。生成时按当前字段顺序动态算列字母，不要硬编码。

字体加粗，底色浅灰填充。其他 sheet 类型（单存储 / 网络安全 / 按量）按各自字段顺序同理推导。

## 三、跨 sheet 总览（可选）

策略 B/C 推荐加一个 "总览" sheet：

| 项 | 月总价 | 周期总价 |
| --- | --- | --- |
| ECS+RDS 报价 | `='ECS+RDS 报价'!K{合计行}` | `='ECS+RDS 报价'!M{合计行}` |
| 单存储与流量 | ... | ... |
| 网络与安全 | ... | ... |
| **合计**（不含按量）| `=SUM(...)` | `=SUM(...)` |
| 按量计费（参考估算）| ... | —— |

## 四、"假设与说明" sheet

固定一个 sheet，结构（key-value 两列）：

| 项 | 值 |
| --- | --- |
| 地域默认 | 华东2(上海) |
| ECS 代次默认 | 最新代次 + Intel (g4i/c4i/r4i) |
| 系统盘默认 | 极速型 SSD PL0 0.5 元/GiB/月 |
| 数据盘默认 | 极速型 SSD FlexPL 1.0 元/GiB/月 |
| 计费方式默认 | 包1年 |
| 包1年月折算 | 包1年总价 / 12 |
| 隐藏成本 | 公网带宽/备份/跨可用区流量 默认不计入 |
| 缺规格的假设 |（逐行列每项产品的假设） |
| 无对标的产品 |（逐行列每个产品 + 候选）|
| 数据源 | 本地 CSV `../火山产品刊例价/`，最新更新日期 YYYY-MM-DD |

## 五、openpyxl 代码骨架

> 这是 **Python `openpyxl`** 的参考实现(代理无关,任何 Python 环境装上即用)。换语言/库(如 Node `exceljs`、Go `excelize`)按各自 API 套同样字段顺序、公式和配色规则即可。

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = Workbook()
wb.remove(wb.active)  # 删除默认 sheet

# ========== 品牌分区配色 (见第六章) ==========
PALETTE = {
    "ali":     {"hdr": "C56B2D", "data": "FFF1E3", "tot": "F5C99A"},
    "vol":     {"hdr": "2E5C9E", "data": "EAF2FB", "tot": "B7CFEB"},
    "neutral": {"hdr": "595959", "data": "FAFAFA", "tot": "D9D9D9"},
}
WHITE_BOLD = Font(bold=True, color="FFFFFF")
DARK       = Font(color="1F1F1F")
DARK_BOLD  = Font(bold=True, color="1F1F1F")
THIN = Side(border_style="thin", color="BFBFBF")
BORDER = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)

def classify_column(header: str) -> str:
    """根据列名分到 ali / vol / neutral 三组之一 (见第六章规则)"""
    if not header:
        return "neutral"
    h = header.split("(")[0].strip()
    if h.startswith("阿里"):
        return "ali"
    VOL_NAMES = {
        "火山产品", "火山规格", "实例月单价", "存储月单价", "单台月价",
        "月总价", "周期总价", "配置说明", "存储类型", "容量单价",
        "规格/套餐", "月单价", "单价", "计费维度",
    }
    if h.startswith("火山") or h in VOL_NAMES:
        return "vol"
    return "neutral"

def fill(hex_): return PatternFill("solid", fgColor=hex_)

def add_sheet(title, headers, rows, total_cols):
    """
    title: sheet 名
    headers: 列名 list (字段顺序见第一章)
    rows: list of dict (key 同 headers, value 可以是常量或公式字符串以 = 开头)
    total_cols: 需要 SUM 合计的列 index list (0-based)
    """
    ws = wb.create_sheet(title)
    groups = [classify_column(h) for h in headers]

    # 表头行 (深色 + 白字粗体)
    for ci, h in enumerate(headers, 1):
        c = ws.cell(1, ci, h)
        c.fill = fill(PALETTE[groups[ci-1]]["hdr"])
        c.font = WHITE_BOLD
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BORDER
    ws.row_dimensions[1].height = 30

    # 数据行 (浅色 + 深字)
    for ri, row in enumerate(rows, 2):
        for ci, h in enumerate(headers, 1):
            v = row.get(h, "")
            c = ws.cell(ri, ci, v)
            c.fill = fill(PALETTE[groups[ci-1]]["data"])
            c.font = DARK
            c.border = BORDER
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    # 合计行 (中色 + 深字粗体)
    total_row = len(rows) + 2
    for ci, h in enumerate(headers, 1):
        c = ws.cell(total_row, ci)
        c.fill = fill(PALETTE[groups[ci-1]]["tot"])
        c.font = DARK_BOLD
        c.border = BORDER
        c.alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(total_row, 1).value = "合计"  # 或放在"配置说明"列
    for ci in total_cols:
        col_letter = get_column_letter(ci + 1)
        ws.cell(total_row, ci + 1).value = f"=SUM({col_letter}2:{col_letter}{total_row-1})"

    # 列宽 / 冻结
    for ci, h in enumerate(headers, 1):
        ws.column_dimensions[get_column_letter(ci)].width = max(12, len(str(h)) * 2)
    ws.freeze_panes = "A2"
    return ws

# 示例 rows (公式用相对引用,不要硬算):
# {"实例月单价": "=2088/12", "存储月单价": "=0.5*100", "单台月价": "=G2+H2",
#  "数量": 1, "月总价": "=I2*J2", "周期总价": "=K2*12"}
```

**关键约束**:
- 派生列(单台月价、月总价、周期总价、月折算)一律 **写公式**,不要 Python 算好填值。
- 公式中引用其他 cell 必须用绝对/相对 cell 引用(如 `=G2+H2`),不要写 `=240+800`。
- 数量、容量、单价这种"叶子"值,**填数字**(不要写文本)。

## 六、品牌分区配色 (Brand Palette)

云迁移场景下,为了让客户一眼分辨"原云 vs 火山",所有报价/对照 sheet 的**列**按下表归到三个色系:

### 1. 三组配色 (WCAG AA 对比度均 ≥ 4.5:1)

| 组 | 表头 (深色,白字粗) | 数据 (浅色,深字) | 合计 (中色,深字粗) |
| --- | --- | --- | --- |
| **阿里 / 友商** (暖橙系) | `#C56B2D` | `#FFF1E3` | `#F5C99A` |
| **火山引擎** (冷蓝系) | `#2E5C9E` | `#EAF2FB` | `#B7CFEB` |
| **中性** (灰系) | `#595959` | `#FAFAFA` | `#D9D9D9` |

字体色:深色背景用 `#FFFFFF` 粗;浅/中色背景用 `#1F1F1F`(合计粗体)。

### 2. 列分组规则(基于列名,不基于位置 — 加新字段不破坏分组)

```
if 列名 startswith "阿里"           → ali
elif 列名 startswith "火山"          → vol
elif 列名 in {火山产品, 火山规格, 实例月单价, 存储月单价, 单台月价,
              月总价, 周期总价, 配置说明, 存储类型, 容量单价,
              规格/套餐, 月单价, 单价, 计费维度}   → vol
else                                  → neutral
```

逻辑:友商原始信息走 ali;火山产品 + 火山报价计算结果走 vol;数量、容量、计费周期、地域、备注、估算说明、单位、等价度这些"中立元信息"走 neutral。

### 3. 各字段集 (四种 sheet 类型) 的分组结果

**实例 + 存储二元** (15 列):
- ali: 阿里产品, 阿里规格
- vol: 火山产品, 火山规格, 配置说明, 实例月单价, 存储月单价, 单台月价, 月总价, 周期总价
- neutral: 类别, 数量, 计费周期, 地域, 备注

**单存储**:
- ali: 阿里产品, 阿里规格
- vol: 火山产品, 存储类型, 容量单价, 月总价, 周期总价
- neutral: 容量(GiB), 计费周期, 地域, 备注

**网络/安全**:
- ali: 阿里产品, 阿里规格
- vol: 火山产品, 规格/套餐, 月单价, 月总价, 周期总价
- neutral: 数量, 计费周期, 地域, 备注

**按量计费**:
- ali: 阿里产品, 阿里规格
- vol: 火山产品, 火山规格, 计费维度, 单价
- neutral: 单位, 估算说明, 地域, 备注

**产品对照表**:
- ali: 阿里云产品, 阿里规格
- vol: 火山引擎产品, 火山规格
- neutral: 等价度, 备注

**假设与说明**:
- 全 neutral(纯说明 sheet,key 列用 `tot` 中灰加粗,value 列用 `data` 近白)

### 4. 场景 2 (非云迁移) 的处理

场景 2 没有"阿里产品/阿里规格"列,自然没有 ali 列。其余 vol/neutral 分组不变,色系一致。

### 5. 应用方式

在 `add_sheet()` 内由 `classify_column(header)` 自动分组并涂色(见第五章代码骨架)。**不要**手工逐 cell 调色——分组规则要么改 `classify_column` 集中处理。

## 七、文件命名与输出

- 文件名：`<客户名>-火山引擎报价-YYYYMMDD.xlsx`
- 输出位置：优先客户目录（与 `Skills/` 同级的 `<客户名>/`，如 `../../<客户名>/`），否则当前工作目录。
- 不覆盖旧文件：同日已有则加 `-v2` `-v3` 后缀。

## 八、验收 checklist（生成后必查）

- [ ] 每个 sheet 表头底色一致、冻结首行。
- [ ] 每行的派生列点开是公式（不是死值）。
- [ ] 合计行的 SUM 范围覆盖全部数据行。
- [ ] 备注列里所有"待补"/"假设"/"无对标"的行有明文说明。
- [ ] "假设与说明" sheet 不为空。
- [ ] 场景 2 模式的报价 sheet 没有"阿里产品/阿里规格"列。
- [ ] 跨 sheet 总览（如有）的引用单元格地址正确，不报 #REF!。
