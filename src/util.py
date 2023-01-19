#! /usr/bin/env python3
#  -*- coding: utf-8 -*-

import MySQLdb
import urllib.parse
from youtubesearchpython import Video, VideosSearch
# from pprint import pprint

NOT_PLAYING = 'NOT_PLAYING'
PLAYING = 'PLAYING'
PLAYED = 'PLAYED'

class DBManager:
    def __init__(self, server):
        self.connect()
        self.server = server
        pass

    def connect(self):
        """
        DBに接続
        """
        self.connection = MySQLdb.connect(
            host='mysql-svc',
            port=3306,
            user='root',
            passwd='mysql',
            db='rhythmdb')
        self.cursor = self.connection.cursor()
        return

    def add(self, url, author):
        """
        キューを追加
        """
        query = f"INSERT INTO queue (url, server, author, status) VALUES ('{url}', '{self.server}', '{author}', '{NOT_PLAYING}')"
        self.cursor.execute(query)
        self.connection.commit()
        return

    def play(self):
        """
        ステータスを「再生中」に
        """
        # 再生中のものがあるか確認
        def is_playing():
            query = f"SELECT count(1) FROM queue WHERE server='{self.server}' AND status='{PLAYING}'"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return int(rows[0][0]) > 0

        # 次に再生すべき、未使用のキューのidとurlを1つ拾ってくる
        def get_next_queue():
            query = f"SELECT id, url FROM queue WHERE server='{self.server}' AND status='{NOT_PLAYING}' ORDER BY id ASC LIMIT 1"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows

        # 次に再生すべき動画のステータスをPLAYINGに変更する
        def update(id):
            query = f"UPDATE queue SET status='{PLAYING}' WHERE id={id}"
            self.cursor.execute(query)
            self.connection.commit()
            return

        # 再生中ではないことが前提
        if not is_playing():
            rows = get_next_queue()
            # 未使用のキューが拾って来れなかったら、Noneを返すA
            if rows is not None and isinstance(rows, list) and len(rows) == 2:
                id, url = rows
                update(id)
                return url
        return None

    def played(self, id):
        """
        ステータスを「再生終了」に
        """
        query = f"UPDATE queue SET status='{PLAYED}' WHERE id={id}"
        self.cursor.execute(query)
        self.connection.commit()
        return

    # TODO:
    # チャンネルからdisconnectしたとき、queueを全てplayedにする
    def played(self):
        """
        ステータスをすべて「再生終了」に
        """
        query = f"UPDATE queue SET status='{PLAYED}' WHERE server='{self.server}'"
        self.cursor.execute(query)
        self.connection.commit()
        return

    def disconnect(self):
        """
        DBから切断
        """
        # 接続を閉じる
        self.connection.close()
        return


class Info:
    def __init__(self, video=None, author='anonimous'):
        if video is None:
            self.title = None
            self.url = None
            self.id = None
        else:
            self.set_info(video)
            self.author = author
        print('author:', self.author)
        return
    
    def set_info(self, video):
        # print(video)
        # duration.secondsText
        self.title = video['title']
        self.url = video['link']
        self.id = video['id']
        secondsText = video['duration']['secondsText']
        sec = int(secondsText)
        h = sec // 3600
        sec = sec % 3600
        m = sec // 60
        s = sec % 60
        if h > 0:
            self.duration = f'{h}:{m}:{s}'
        else:
            self.duration = f'{m}:{s}'
        return
    
    def __str__(self):
        return f'[{self.title}]({self.url}) | `{self.duration} Requested by: {self.author}`'

def get_movie_id_from_youtube_url(anURL, author):
    # print(anURL)
    videos = VideosSearch(anURL)
    # pprint(videos.result())
    parsed = urllib.parse.urlparse(anURL)
    # info = {}
    id = None
    if parsed.netloc == 'www.youtube.com':
        param_dict = urllib.parse.parse_qs(parsed.query)
        id = param_dict['v'][0]
    elif parsed.netloc == 'youtu.be':
        id = parsed.path.split('/')[1]
    else:
        raise UrlParseError('URLをうまく解析できませんでした。YouTubeのURLではない可能性があります。')
    video = Video.getInfo(f'https://www.youtube.com/watch?v={id}')
    info = Info(video, author)
    # print(video)
    return info

def test():
    print('動作検証モード')
    src1 ='https://www.youtube.com/watch?v=C9uUVLE5cuY&list=RDMMuvANVr11r4I&index=3'
    src2 = 'https://youtu.be/0YzA7sSlM-M'
    src3 = 'https://www.youtube.com/watch?v=TO0_MTcfqo4&list=RDGMEMXdNDEg4wQ96My0DhjI-cIgVMTO0_MTcfqo4&start_radio=1'
    src4 = 'https://youtu.be/qsl6aDhSBVQ?list=RDqsl6aDhSBVQ'
    id1 = get_movie_id_from_youtube_url(src1)
    id2 = get_movie_id_from_youtube_url(src2)
    id3 = get_movie_id_from_youtube_url(src3)
    id4 = get_movie_id_from_youtube_url(src4)

    print(src1, id1)
    print(src2, id2)
    print(src3, id3)
    print(src4, id4)

class UrlParseError(Exception):
    pass

if __name__ == '__main__':
    test()