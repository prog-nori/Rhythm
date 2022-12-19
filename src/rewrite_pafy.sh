SED=$(which sed)
TARGET=/usr/local/lib/python3.11/site-packages/pafy/backend_youtube_dl.py

LIKE_OLD="self._likes = self._ydl_info['like_count']"
LIKE_NEW="self._likes = self._ydl_info.get('like_count', 0)"

DISLIKE_OLD="self._dislikes = self._ydl_info.get('dislike_count', 0)"
DISLIKE_NEW="self._dislikes = self._ydl_info['dislike_count']"

echo "$TARGETにて。"
echo "$SEDコマンドで$LIKE_OLDを$LIKE_NEWに書き換えます。"
echo "$SEDコマンドで$DISLIKE_OLDを$DISLIKE_NEWに書き換えます。"

$SED "53s/$LIKE_OLD/$LIKE_NEW/g" $TARGET
$SED "54s/$DISLIKE_OLD/$DISLIKE_NEW/g" $TARGET


# self._likes = self._ydl_info.get('like_count', 0)
# self._dislikes = self._ydl_info.get('dislike_count', 0)

# self._likes = self._ydl_info['like_count']
# self._dislikes = self._ydl_info['dislike_count']