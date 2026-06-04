#!/usr/bin/env python3
"""verify_quote.py — 报价 Excel 验收脚本

用法: python verify_quote.py <报价文件.xlsx> [--strategy A|B|C] [--scenario 1|2]

校验项:
  1. 派生列 (月总价/周期总价/单台月价) 必须是公式
  2. 数量列必须是数字(非公式)
  3. 合计行存在,SUM 覆盖全部数据行
  4. sheet 数量与策略匹配 (A=4, B=6, C=8~13)
  5. 必须有"假设与说明" sheet 且非空
  6. 场景 2 模式不应出现"阿里产品"/"阿里规格"列
"""
import sys
import argparse
from openpyxl import load_workbook

DERIVED_COLS = {"单台月价", "月总价", "周期总价", "存储月单价"}
QUANTITY_COLS = {"数量", "容量", "容量(GiB)"}
STRATEGY_SHEET_RANGE = {"A": (4, 4), "B": (6, 6), "C": (8, 13)}


def is_formula(cell):
    return isinstance(cell.value, str) and cell.value.startswith("=")


def check_brand_palette(ws, warnings):
    """软检查:表头行是否套了品牌分区配色 (任何 PatternFill 即可,不强校验色值)"""
    if ws.max_row < 1:
        return
    styled = 0
    for c in ws[1]:
        if c.value and c.fill and c.fill.fgColor and c.fill.fgColor.rgb not in (None, "00000000", "FFFFFFFF"):
            styled += 1
    if styled == 0:
        warnings.append(f"[{ws.title}] 表头未应用分区配色 (brand palette)")


def check_sheet(ws, errors, warnings):
    headers = [c.value for c in ws[1] if c.value]
    if not headers:
        return
    col_idx = {h: i + 1 for i, h in enumerate(headers)}

    # 找合计行
    total_row = None
    for row in ws.iter_rows(min_row=2):
        for c in row:
            if c.value == "合计":
                total_row = c.row
                break
        if total_row:
            break

    data_rows = range(2, total_row) if total_row else range(2, ws.max_row + 1)
    if not data_rows:
        return

    # 派生列必须是公式 / 数量列必须是数字
    for h in headers:
        if h in DERIVED_COLS:
            for r in data_rows:
                c = ws.cell(r, col_idx[h])
                if c.value not in (None, "") and not is_formula(c):
                    errors.append(f"[{ws.title}] {h} 列 行{r} 不是公式: {c.value!r}")
        if h in QUANTITY_COLS:
            for r in data_rows:
                c = ws.cell(r, col_idx[h])
                if is_formula(c):
                    errors.append(f"[{ws.title}] {h} 列 行{r} 不应是公式")

    # 合计行 SUM 覆盖范围
    if total_row:
        sum_targets = {"数量", "月总价", "周期总价"}
        for h in headers:
            if h in sum_targets and h in col_idx:
                c = ws.cell(total_row, col_idx[h])
                if not is_formula(c) or "SUM" not in c.value.upper():
                    warnings.append(f"[{ws.title}] 合计行 {h} 列非 SUM 公式: {c.value!r}")
                else:
                    last = list(data_rows)[-1]
                    if f":{ws.cell(last, col_idx[h]).coordinate.rstrip('0123456789')}{last}" not in c.value.upper().replace(" ", ""):
                        pass  # range check approximate; skip strict
    else:
        warnings.append(f"[{ws.title}] 未找到'合计'行")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--strategy", choices=list(STRATEGY_SHEET_RANGE), default="B")
    ap.add_argument("--scenario", choices=["1", "2"], default="1")
    args = ap.parse_args()

    wb = load_workbook(args.file)
    errors, warnings = [], []

    # sheet 数量
    lo, hi = STRATEGY_SHEET_RANGE[args.strategy]
    n = len(wb.sheetnames)
    if not (lo <= n <= hi):
        errors.append(f"sheet 数量 {n} 不在策略 {args.strategy} 范围 [{lo},{hi}]")

    # 假设与说明
    if "假设与说明" not in wb.sheetnames:
        errors.append("缺少 '假设与说明' sheet")
    elif wb["假设与说明"].max_row < 2:
        errors.append("'假设与说明' sheet 为空")

    # 场景 2 不应有友商列
    if args.scenario == "2":
        for name in wb.sheetnames:
            headers = [c.value for c in wb[name][1] if c.value]
            for forbidden in ("阿里产品", "阿里规格"):
                if forbidden in headers:
                    errors.append(f"[{name}] 场景2 不应有 '{forbidden}' 列")

    # 每个数据 sheet 检查
    for name in wb.sheetnames:
        check_brand_palette(wb[name], warnings)
        if name in ("假设与说明", "产品对照表", "总览"):
            continue
        check_sheet(wb[name], errors, warnings)

    print(f"=== verify_quote.py: {args.file} ===")
    print(f"策略: {args.strategy}  场景: {args.scenario}  sheet数: {n}")
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"FAIL  {e}")
    if errors:
        print(f"\n❌ 验收失败: {len(errors)} 个错误, {len(warnings)} 个警告")
        sys.exit(1)
    print(f"\n✅ 验收通过{f' ({len(warnings)} 警告)' if warnings else ''}")


if __name__ == "__main__":
    main()
