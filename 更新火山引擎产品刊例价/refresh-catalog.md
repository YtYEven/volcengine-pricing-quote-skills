# 刷新产品目录 (product_catalog.md)

> 火山引擎的产品列表会变（新品上线、老品下架、代号改名）。本文档说明何时、如何重建 [product_catalog.md](product_catalog.md)。

## 何时触发

满足以下任一条件就该跑一次：
- 用户明确说"先刷新产品列表"、"更新一下产品目录"、"对齐最新产品"。
- 距离上次刷新超过 **30 天**（看 `product_catalog.md` 文件 mtime）。
- 全量更新时遇到 ≥ 3 个产品 `?product=<Code>` 回落到 ECS 页面（说明代号过期）。
- 用户报告了一个不在 catalog 里的产品名。
- 火山引擎官网做过重大改版（用户提到 / 你访问时发现）。

## 不要每次都跑

刷新本身要遍历整站定价导航，耗时不短。除非满足上面任一条件，**默认沿用本地 catalog**。SKILL 主流程不要把它当强制前置步骤。

## 刷新流程

### Step 1 — 抓取产品入口列表

**浏览器导航**到定价总入口:`https://www.volcengine.com/pricing`

等待 3 秒，然后 evaluate 抓侧边栏 / 产品导航的所有定价链接：
```js
async () => {
  await new Promise(r => setTimeout(r, 3000));
  const links = [...document.querySelectorAll('a[href*="pricing?product="]')];
  const seen = new Map();
  for (const a of links) {
    const url = new URL(a.href, location.origin);
    const code = url.searchParams.get('product');
    const name = a.textContent?.trim();
    if (code && name && !seen.has(code)) seen.set(code, name);
  }
  return [...seen.entries()].map(([code, name]) => ({code, name}));
}
```

> 如果侧边栏是按分类折叠的，先把每个一级分类展开（`.click()` 所有 `[role="button"]` 或 `details > summary`）再抓。
> 如果 `a[href*="pricing?product="]` 选不全，回退到抓 `main.innerText` 然后正则 `/product=([A-Za-z_-]+)/` 找代号，再人工 / 模糊对名字。

### Step 2 — 与本地 catalog 对账

读 `product_catalog.md` 解析出现有 (中文名, 代号) 列表，然后跟 Step 1 抓到的对照：

- **新增**：抓到但本地没有 → 新产品，候选加入。
- **失踪**：本地有但抓不到 → 可能改名/下架。先用代号直接打开 `?product=<Code>&tab=1` 验证，仍能正常出价格表就保留；否则标为 "待确认/可能下架"。
- **改名**：代号相同但中文名变了 → 以官网为准更新。

### Step 3 — 分类（download / snapshot）

对 **新增** 的产品逐个：
1. 打开 `?product=<Code>&tab=1`，切到官网刊例价。
2. 探测有无"价格下载"按钮：
   ```js
   async () => {
     await new Promise(r => setTimeout(r, 2500));
     const btns = [...document.querySelectorAll('button, a, span, div')];
     for (const b of btns) {
       if (b.textContent?.trim() === '价格下载' && b.offsetParent !== null) return 'download';
     }
     return 'snapshot';
   }
   ```
3. 注意 veRTC 类陷阱：按钮存在但点击不下载。新增产品建议 **真点一次** 验证（用 baseline `ls ~/Downloads | wc -l` 对比），把假按钮的产品归到 snapshot。

### Step 4 — 重写 product_catalog.md

按 download / snapshot 两张表写回去，保留：
- 中英文名映射。
- snapshot 列的"备注"列（说明特殊情况）。
- 底部"模糊匹配"小节（用户给昵称/英文缩写时的等价规则）。

写完后用 `ls ../火山产品刊例价/` 看一遍现有 CSV 产品名，确保 catalog 覆盖完整（已有 CSV 但不在 catalog 里说明遗漏了）。

### Step 5 — 汇报差异

向用户输出一段简明 diff：
- 新增 N 个产品：列名字
- 失踪 N 个产品：列名字 + 是否仍可访问
- 代号改动 N 个：旧 → 新

让用户确认要不要顺带把新增产品也跑一遍刊例价更新。

## 注意

- catalog 是 **决策来源**，不是 **数据源**。catalog 错了，主流程会把错产品的 CSV 写错地方。所以宁可花时间刷一次 catalog，也不要凭印象改主流程。
- 永远不要从 catalog 里删掉本地 CSV 还存在的产品。如果官网真下架了某产品，把 catalog 留一行加 `备注: 已下架` 标记，让主流程跳过它即可 —— 历史 CSV 由用户决定何时清理。
