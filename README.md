# ETF 下跌加碼計算器

自動抓取 SMH / 00981A / VOO 歷史最高點與今日收盤，計算下跌加碼價位。

## 部署步驟（5 分鐘）

### 1. 上傳到 GitHub

1. 登入 [github.com](https://github.com)
2. 右上角 `+` → `New repository`
3. Repository name 填 `etf-tracker`
4. 選 **Public**，按 `Create repository`
5. 把這整個資料夾的檔案上傳進去（拖拉上傳即可）

### 2. 部署到 Vercel

1. 登入 [vercel.com](https://vercel.com)（用 GitHub 帳號登入）
2. 按 `Add New → Project`
3. 選你剛建的 `etf-tracker` repository → `Import`
4. **Framework Preset** 選 `Other`
5. **Root Directory** 不用改
6. 按 `Deploy`
7. 等 1 分鐘 → 拿到網址，例如 `etf-tracker.vercel.app`

### 3. 完成！

打開網址，選 ETF，按「自動抓取」就可以用了。

## 檔案結構

```
etf-tracker/
├── api/
│   └── quote.py        ← 後端 API（抓 Yahoo Finance）
├── public/
│   └── index.html      ← 前端介面
└── vercel.json         ← Vercel 設定
```

## 注意事項

- 資料來源：Yahoo Finance 公開 API（免費，無需 key）
- 00981A 為台股 ETF，收盤時間為台灣時區下午 1:30
- ATH 以近 5 年最高收盤價計算
