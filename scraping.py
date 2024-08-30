from bs4 import BeautifulSoup
import requests
import datetime
import webbrowser

#URL
action_url = "https://www.release.tdnet.info/onsf/TDJFSearch/"

#日付
today = datetime.date.today()
yyyymmdd = today.strftime('%Y%m%d')
#必要に応じて、変更する。
t0 = "20230901"
t1 = "20230910"

#t0 = yyyymmdd
#t1 = yyyymmdd





#キーワード
keyword = "優待"

# POSTデータ
form_data = {
    "t0": t0,  # 検索期間の開始日
    "t1": t1,  # 検索期間の終了日
    "q": keyword,   # キーワード検索のクエリ
    "m": "0",          # 隠しフィールド
}

# POSTリクエストを送信
response = requests.post(action_url, data=form_data)

# レスポンスのHTMLを解析
soup = BeautifulSoup(response.content, 'html.parser')

# 結果件数を抽出
result_count = soup.find('span', id='result').text
# テーブルから情報を抽出
table = soup.find('table', id='maintable')
rows = table.find_all('tr', class_=True)

# ファイル名を指定してテキストファイルを開く
with open("output.txt", "r", encoding="utf-8") as file:
    existing_content = file.read()

#件数
i = 0

# 各行から情報を抽出
for row in rows:
    time = row.find('td', class_='time').text
    code = row.find('td', class_='code').text
    companyname = row.find('td', class_='companyname').text
    pdf_link = row.find('a')['href'] if row.find('a') else "N/A"
    _link = "https://www.release.tdnet.info/"
    
    new_entry = f"時刻: {time}\nコード: {code}\n会社名: {companyname}\nPDFリンク: {_link + pdf_link}\n\n"


    # すでにファイルに同じ内容が含まれていない場合にのみ追記する
    if new_entry not in existing_content:
        # ファイルに情報を追記する
        with open("output.txt", "a", encoding="utf-8") as file:
            file.write(new_entry)
        i+=1
        print(result_count + "件中" + str(i) + "件情報をファイルに保存しました。" )
       # URLを開く
        webbrowser.open(_link + pdf_link)
    else:
        i+=1
        print(str(i) + "件書き込みに失敗しました。")
# ファイルを閉じる
file.close()

