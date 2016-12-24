#!/usr/bin/python3
#coding: utf-8

import sys, json, random, os
import urllib.request
from bs4 import BeautifulSoup
import re
import MeCab

# 歌詞サイトをダウンロード(shift-jis)する関数
def url_access(url):
    res = urllib.request.urlopen(url)
    data = res.read()
    text = data.decode("utf-8") # バイナリから文字列に変換
    return text

# BeautifulSoup で html を解析 (タイトルと歌詞リンクを抽出)する関数
def get_lyrics():
    url = "http://j-lyric.net/artist/a000723/"

    f = open('lyrics.txt', 'w', encoding='utf-8') # 書き込むためのファイルを生成
    sys.stdout = f # 標準出力をファイルに換える

    text = url_access(url)
    soup = BeautifulSoup(text, 'html.parser')

    url = "http://j-lyric.net"
    
    links = soup.find_all("a")
    for a in links:
        href = a.attrs['href']
        title = a.string
        if href.find("http") == -1 and href.find("artist/a000723/") != -1:
            text = url_access(url + href) # 歌詞サイトへアクセス
            soup = BeautifulSoup(text, 'html.parser')
            lyric = soup.find(id="lyricBody")
            print (lyric) # 歌詞をファイルへ出力 ( > file)
    f.close()

# 歌詞ファイルから歌詞のみを抽出する関数
def extract_lyrics():
    f1 = open('lyrics.txt', 'r', encoding='utf-8') # ファイルの読み込み
    Allf = f1.read()

    text = Allf.replace('\n', '')
    text = text.replace('<br/>', '')
    text = text.replace('</p>', '')
    text = text.replace('<p id="lyricBody">', '')

    f2 = open('larc_lyrics.txt', 'a') # ファイルの書き込み
    f2.write(text)

    f1.close()
    f2.close()

# マルコフ連鎖の辞書を作成し，歌詞を出力する関数
def create_dic():
    word_dic = {}
    w1 = ""
    # w2 = "" # 2重マルコフ連鎖の場合有効にする
    
    f1 = open('larc_lyrics.txt', 'r') # 歌詞ファイルを指定
    text = f1.read()
    f1.close()
    
    #mecab = MeCab.Tagger("-Ochasen")
    mecab = MeCab.Tagger("-Owakati")
    malist = mecab.parse(text)
    malist = malist.rstrip("\n").split(" ") # 空行削除し，スペースで区切る

    for word in malist: # 辞書の作成
        if w1:
            if w1 not in word_dic:
                word_dic[w1] = []
            word_dic[w1].append(word)
        w1 =  word
    #print (word_dic)

    # マルコフ連鎖により自動生成した歌詞を出力
    w1 = random.choice(list(word_dic.keys()))

    for i in range(0, 10):
        count = 0
        sentence = ""
        while count < 10:
            tmp = random.choice(word_dic[w1])
            if re.search(r'^[a-zA-Z]*', tmp).end() != 0:
                sentence += " " + tmp + " "
            else:
                sentence += tmp
            w1 = tmp
            count += 1
        print (sentence) 

# 2重マルコフ連鎖の場合有効にする。
"""
    for word in malist: # 辞書の作成
        if w1d w2:
        if w1 and w2:
            if (w1, w2) not in word_dic:
                word_dic[(w1, w2)] = []
            word_dic[(w1, w2)].append(word)
        w1, w2 = w2, word
    #print (word_dic)

    # マルコフ連鎖により自動生成した歌詞を出力
    w1, w2 = random.choice(list(word_dic.keys()))

    for i in range(0, 10):
        count = 0
        sentence = ""
        while count < 14:
            tmp = random.choice(word_dic[(w1, w2)])
            if re.search(r'^[a-zA-Z]*', tmp).end() != 0:
                sentence += " " + tmp + " "
            else:
                sentence += tmp
            w1, w2 = w2,tmp
            count += 1
        print (sentence + "\n") 
"""

if __name__ == "main":
    #get_lyrics() # 歌詞サイトへアクセスし，歌詞を取得
    #extract_lyrics() # 歌詞を抽出し，ファイルへ書き込み
    create_dic() # マルコフ連鎖の辞書を作成し，適当な歌詞を出力
