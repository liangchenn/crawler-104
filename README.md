# 104 求職網爬蟲

## Synopsis

- 104 求職網當日工作數量爬蟲
  - 按照不同縣市、區域
  - 按照不同工作經驗
  - 按照不同工作型態

- 執行完成後，會在 `data/` 路徑下產生資料
  e.g. `data/result-2021-07-03.csv`

- 當前資料夾下有 `test.ipynb`，可以觀察目前的資料結果長相以及爬蟲運作
  
  - 打開方式為：打開 powershell
    ```
    # change for your dir path
    $ cd D:\User_data\Desktop\crawlers\crawler-104
    $ jupyter notebook
    ```
  - 這樣會打開一個網頁可以再打開 ipython notebook 格式的檔案，也可以在裡面執行 python 程式。

## Method

- 目前因為求職網最多只能出現一百頁的資料，一頁最多 30 筆。因此全部只能得到 3000 筆資料。
  若把地區設定地比較大 e.g. 台北市所有區，很容易超過而無法得到所有工作資料。

- 因此此處是進入每一個地區、每一種工作經驗要求的頁面，然後取得最上方的工作總數總計。
  - 分有 全部、全職、兼職、高階、派遣 等類型

- 104 的網址可以組成各種篩選條件，主要透過 `?` 的 query 來調整
  - 工作經驗 `jobexp` : 分有 `[1, 3, 5, 10, 99]` ，代表不拘、1-3年，一直到 10 年以上
  - 更新日期 `isnew`  : 本日更新 `isnew=0`
  - 區域 `area` : 須知道所有分區的編碼，這邊已建立 `mapping.json` 來對照


## Usage

### Main

如下，至命令列介面（e.g. Powershell） 執行主要爬蟲程式

```{py=}
$ python3 crawler.py
```

## preprocess
- install necessary modules
  ```
  $ pip install -r requirements.txt
  ```

- obtain area codes for 104 website
  ```
  $ python3 mapping.py
  ```


## Files

### Structure
```
.
├── README.md
├── crawler.py
├── data/
├── mapping.json
├── mapping.py
├── requirements.txt
├── test.ipynb
└── work.log
```
### Descrption
- `REAME.md` : 說明文件
- `crawler.py` : 主要爬蟲程式
- `data/` : 每日資料儲存區
- `mapping.py` : 取得地區與網頁編碼的對照程式
- `mapping.json` : 地區與網頁編碼的對照資料
- `requirements.txt` : 需要的Python套件
- `test.ipynb` : 測試用 Jupyter 筆記本
- `work.log` : 程式執行紀錄
- `exception.log` : 程式錯誤紀錄（有錯才會出現）




