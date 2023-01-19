# MySQLdbのインポート
import MySQLdb
 
# データベースへの接続とカーソルの生成
connection = MySQLdb.connect(
    host='mysql-svc',
    port=3306,
    user='root',
    passwd='mysql',
    db='rhythmdb')
cursor = connection.cursor()
 
# ここに実行したいコードを入力します

cursor.execute("SELECT count(*) FROM unchi")

# 保存を実行
connection.commit()
 
# 接続を閉じる
connection.close()