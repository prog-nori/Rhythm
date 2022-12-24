#! /usr/bin/env python3
#  -*- coding: utf-8 -*-

# import asyncio
import nest_asyncio
import pafy

from discord import (
    Client,
    Embed,
    FFmpegPCMAudio,
    Intents
)
from settings import TOKEN
from util import get_movie_id_from_youtube_url, UrlParseError, Info

nest_asyncio.apply()

FFMPEG_OPTIONS = {'-codec:a': 'libmp3lame'}
# FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

intents = Intents.default()  # デフォルトのIntentsオブジェクトを生成
intents.typing = True  # typingを受け取らないように
intents.message_content=True
client = Client(intents=intents)

# loop = asyncio.get_event_loop()

music_queue = []
current = None

@client.event
async def on_ready():
    print('Botを起動しました。')

@client.event
async def on_message(message):
    global current, music_queue
    msg = message.content
    if message.author.bot:
        return
    
    def play():
        global current
        # source = FFmpegPCMAudio(music)
        if not music_queue or \
            not message.guild.voice_client or \
            message.guild.voice_client.is_playing():
            return
        current = music_queue.pop(0)
        audio = pafy.new(current.id).getbestaudio()
        src = FFmpegPCMAudio(audio.url)
        message.guild.voice_client.play(src, after=lambda e:play())
    
    if msg[:5] == '!play' or msg[:2] == '!p':

        if message.author.voice is None:
            await client.send_message(message.channel ,'ボイスチャンネルに参加してからコマンドを打ってください。')
            return
        if message.guild.voice_client is None:
            await message.author.voice.channel.connect()
            await message.channel.send("接続しました")

        # youtubeからダウンロードし、再生
        try:
            movie_info = get_movie_id_from_youtube_url(msg.split(' ')[-1], message.author)
        except UrlParseError as e:
            await message.channel.send(e)
            return
        music_queue.append(movie_info)
        play()
        if not (message.guild.voice_client.is_playing() or \
            music_queue):
            current = None
        return

    if msg == '!fs' or msg == '!skip':
        if not message.guild.voice_client.is_playing():
            return
        message.guild.voice_client.pause()
        if len(music_queue) > 0:
            play()
        else:
            current = None

    if msg == '!q' or msg == '!queue':
        embed = Embed(title='Queue', description='以下の動画が予約されています', color=0x06c755)
        if current:
            current_body = f'{current}\n\n'
            embed.add_field(name='現在再生中の曲', value=current_body, inline=False)

        body = '\n'.join([f'`{i}.` {q}\n' for i, q in enumerate(music_queue, 1)])

        embed.add_field(name='予約リスト', value=body if len(body) > 0 else 'キューはありません。', inline=False)
        await message.channel.send(embed=embed)
    
    # 再生中の音楽を停止させる
    if msg == '!stop':
        if message.guild.voice_client.is_playing():
            await message.guild.voice_client.pause()
            return
    
    if msg == '!resume':
        if not message.guild.voice_client.is_playing():
            await message.guild.voice_client.resume()
            return

    # botをボイスチャットから切断させる
    if msg == '!disconnect' or msg == '!d':
        if message.guild.voice_client is None:
            await message.channel.send("接続していません。")
            # queueをリセットする
            music_queue = []
            current = None
            return

        # 切断する
        await message.guild.voice_client.disconnect()

        await message.channel.send("切断しました。")

if __name__ == '__main__':
    client.run(TOKEN)
