import json
import requests
from requests_oauthlib import OAuth1
import re
import configure

# 取得したkeyを定義
access_token = configure.access_token
access_token_secret = configure.access_token_secret
consumer_key = configure.consumer_key
consumer_key_secret = configure.consumer_key_secret

# APIの認証
twitter = OAuth1(consumer_key, consumer_key_secret, access_token, access_token_secret)

def normalize_text(text):
  text = re.sub(r'https?://[\w/:%#\$&\?\(\)~`\.=\-…]', "", text)
  text = re.sub('RT', "", text)
  text = re.sub('お気に入り', "", text)
  text = re.sub('まとめ', "", text)
  text = re.sub(r'[!-~]', "", text)
  text = re.sub(r'[:-@]', "", text)
  text = re.sub('\u3000', "", text)
  text = re.sub('\t', "", text)
  text = re.sub('\n', "", text)

  text = text.strip()
  return text

# API取得用のURL
# 日本語のツイートのみ取得
url = "https://stream.twitter.com/1.1/statuses/sample.json?language=ja"

with open('./public_text_twitter.txv', 'a', encoding='utf-8') as f:
  res =requests.get(url, auth=twitter, stream=True)
  for r in res.iter_lines():
    try:
      r_json = json.loads(r)
      text = r_json['text']
      f.write(normalize_text(text) + '\n')
    except:
      continue
