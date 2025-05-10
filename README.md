#  多格式文件轉換工具（Flask Web App）

這是一個使用 Python Flask 框架開發的文件轉換平台，支援以下轉換格式：

-  PDF ➜ Word（.docx）
-  Word ➜ PDF

使用者可透過前端頁面上傳多個檔案，自由選擇轉換模式，並於轉換後取得每個檔案的下載連結，失敗檔案也會一併顯示錯誤原因。

---

##  功能特色

-  多檔上傳與刪除（可動態增減檔案）
-  支援三種常見格式互轉
-  每筆轉換失敗皆提示原因，不影響其他檔案
-  簡潔直覺的網頁介面（HTML+JS）
-  Flask-based，部署容易，可擴充成 API

---

##  專案結構

```
project/
├── pdftoword.py         # 主程式
├── uploads/             # 暫存上傳檔案
├── converted/           # 儲存轉換結果
├── templates/
│   ├── index.html       # 首頁（多檔上傳介面）
│   └── result_list.html # 轉換結果頁
└── README.md
```


