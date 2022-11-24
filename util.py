#! /usr/bin/env python3
#  -*- coding: utf-8 -*-

import urllib.parse
from youtubesearchpython import Video

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
    info = Info(Video.getInfo(f'https://www.youtube.com/watch?v={id}'), author)
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