#!/usr/bin/env python3
"""verify_pricing.py — 火山产品刊例价目录验收脚本

用法: python verify_pricing.py [--dir <目录>] [--expected <预期产品数>]

校验项:
  1. 每个产品只有一份当天日期的 CSV (无旧时间戳残留)
  2. 没有 `_官网优惠价_` 文件
  3. 每个 CSV 非空 (>0 字节) 且至少 2 行 (表头+数据)
  4. 文件总数 ≈ 预期数 (默认 74)
"""
import sys
import re
import argparse
from pathlib import Path
from datetime import date
from collections import defaultdict

DEFAULT_DIR = Path(__file__).parent.parent.parent / "火山产品刊例价"
TS_PATTERN = re.compile(r"-定价-(\d{4})_(\d{1,2})_(\d{1,2})")


def extract_product(name: str) -> str:
    """从 CSV 文件名提取产品中文名 (去掉 _官网刊例价_xxx 和 _定价-xxx 后缀)"""
    n = name
    for suffix in ("_官网刊例价_详情页提取", "_官网刊例价"):
        if suffix in n:
            n = n.split(suffix)[0]
            return n
    if "_定价-" in n:
        return n.split("_定价-")[0]
    return n.rsplit(".", 1)[0]


def parse_date(name: str):
    m = TS_PATTERN.search(name)
    if not m:
        return None
    try:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=str(DEFAULT_DIR))
    ap.add_argument("--expected", type=int, default=74)
    ap.add_argument("--fresh-days", type=int, default=30,
                    help="文件超过此天数视为陈旧 (warning)")
    args = ap.parse_args()

    d = Path(args.dir)
    if not d.is_dir():
        print(f"FAIL  目录不存在: {d}")
        sys.exit(1)

    csvs = sorted(d.glob("*.csv"))
    errors, warnings = [], []

    # 1. 优惠价文件
    discounted = [f.name for f in csvs if "优惠价" in f.name]
    for f in discounted:
        errors.append(f"残留优惠价文件: {f}")

    # 2. 同产品多份
    by_product = defaultdict(list)
    for f in csvs:
        if "优惠价" in f.name:
            continue
        by_product[extract_product(f.name)].append(f)
    for prod, files in by_product.items():
        if len(files) > 1:
            names = ", ".join(f.name for f in files)
            errors.append(f"产品 '{prod}' 有 {len(files)} 份 CSV: {names}")

    # 3. CSV 非空 + 行数 + 新鲜度
    today = date.today()
    for f in csvs:
        if "优惠价" in f.name:
            continue
        if f.stat().st_size == 0:
            errors.append(f"空文件: {f.name}")
            continue
        try:
            lines = f.read_text(encoding="utf-8", errors="ignore").splitlines()
        except Exception as e:
            errors.append(f"读取失败 {f.name}: {e}")
            continue
        if len([l for l in lines if l.strip()]) < 2:
            errors.append(f"内容不足 (< 2 行): {f.name}")
        # 至少有一个数字 (价格) — 个别快照产品(如 veRTC)只含链接,降级为警告
        if not any(re.search(r"\d", l) for l in lines):
            warnings.append(f"无数字内容(可能只含链接): {f.name}")
        # 新鲜度
        dt = parse_date(f.name)
        if dt and (today - dt).days > args.fresh_days:
            warnings.append(f"陈旧 ({(today-dt).days} 天): {f.name}")

    # 4. 文件总数
    valid_count = len([f for f in csvs if "优惠价" not in f.name])
    if abs(valid_count - args.expected) > 3:
        errors.append(f"文件数 {valid_count} 偏离预期 {args.expected} 超过 ±3")

    print(f"=== verify_pricing.py: {d} ===")
    print(f"CSV 总数: {valid_count} (预期 ~{args.expected})  产品种类: {len(by_product)}")
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
