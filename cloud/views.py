from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Cloud
from datetime import datetime


def index(request):
    # return HttpResponse("hello world")
    return render(request, 'index.html')


def result(request):
    if(request.method == "POST"):
        # twitter_id = "todesking"
        twitter_id = request.POST['twitter_id']
        # pic_name = "tode.png"
        pic_name = twitter_id + str(datetime.now()) + ".png"
        cloud = Cloud(twitter_id=twitter_id, pic_name=pic_name)
        mainprocess(twitter_id, pic_name)
        context = {
            'twitter_id': twitter_id,
            'pic_name': pic_name
        }
        cloud.save()
        return render(request, 'result.html', context)
    else:
        return render(request, '/')





import wordcloud
import matplotlib.pyplot as plt

from datetime import datetime

from twitter import Twitter, OAuth
import neologdn
import re
import MeCab
from collections import defaultdict
import sys

api_key = 'Q3PRNOp9UGAHzfxAdkAdQvpcG'
api_secret = 'KB0INgn3EDcA2GnSgxcnDn8CJLK77w4BxnzMHvJiqcNthzsMyP'
access_token_key = '2866319352-Gd2ghcxrpIc8WVZTmOE6MhXpZE0enfqMME29l44'
access_token_secret = 'JwZPGUjHYYplJrg8WOCkXyyZl5qw9ea17ifgLP6ZcoqB8'


def mainprocess(target_user, filename):

    t = Twitter(auth=OAuth(
        access_token_key,
        access_token_secret,
        api_key,
        api_secret,
    ))

    userTweets = [] #tweetの格納先
    # max_id = <一番新しいtweetID>
    count = 200 #一度のアクセスで何件取ってくるか

    # target_user = input()

    # 最初の読み込み
    aTimeLine = t.statuses.user_timeline(screen_name=target_user, count=count)

    for tweet in aTimeLine:
        userTweets.append(tweet['text'])

    tweet_data = list(map(normalize_string, userTweets))

    result_text = []
    result = defaultdict(int)
    mec = MeCab.Tagger("-Ochasen")

    for tw in tweet_data:

        temp = mec.parse(tw).split('\n')

        for t in temp:

            word_data = t.split()
            word = word_data[0]

            stopwords = ['http', 'EOS', 'rt', 'http', 'tweet', 'peing']

            check = [sw in word for sw in stopwords]

            if any(check):
                break

            tow = word_data[-1]

            if tow[0:2] == "名詞" and "非自立" not in tow and "代名詞" not in tow and\
                                                    "数" not in tow and "接尾" not in tow:

                result_text.append(word)

    create_wordcloud(target_user, " ".join(result_text), filename)


def normalize_string(text):
    normalized_text = neologdn.normalize(text).lower()
    replaced_text = re.sub("[!?@「」()、。・（）…/_:;\s]", "", normalized_text)
    # replaced_text = re.sub("[!?@「」()、。（）…/_:;\d\s]", "", normalized_text)
    # replaced_text = re.sub("[!?@「」()、。（）…/_:;\d\sa-zA-Z]", "", normalized_text)

    return replaced_text



def create_wordcloud(user, text, file_name):
    # 環境に合わせてフォントのパスを指定する。
    fpath = "/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc"
    # fpath = "/usr/share/fonts/ja/TrueType/kochi-gothic-subst.ttf"
    stop_words = ['人', 'あと', '感じ','httpst', 'rt', 'com', 'the', 'http', '今日']

    wc = wordcloud.WordCloud(background_color="white",font_path=fpath, width=900, height=500, \
                          stopwords=set(stop_words)).generate(text)

    plt.figure(figsize=(15,12))
    plt.imshow(wc)
    plt.axis("off")
    # file_name = user + str(datetime.now()) + ".png"
    # plt.savefig(file_name)
    # plt.savefig('cloud/static/pictures/' + file_name)
    plt.savefig('cloud/static/pictures/result.png')

