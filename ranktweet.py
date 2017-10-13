#!/usr/bin/env python3
# coding: UTF-8
import re
import urllib.request
from bs4 import BeautifulSoup
import tweepy
from datetime import datetime
import random

# open url
url = "http://c.student.mynavi.jp/cpf/stu_007/photos/detail/1"
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, "html.parser")

# get votes
votes = soup.find("div", attrs={"id": "votes"})
r_vote = re.compile("[0-9]+")
votes = r_vote.search(votes.text)
my_vote = votes.group(0)

# get ranking
rank_texts = soup.select("div.rank_txt > a")
side_nums = soup.find_all("div", attrs={"class": "side_num"})
r_name = re.compile("<a.+</a>")

# get yagapon's rank
for i in range(len(rank_texts)):
    if rank_texts[i].text == "やがぽん":
        yagapon_rank = i
        break

# get datetime
now = datetime.now().strftime("%m/%d %H:%M")
output = "【マスコット総選挙】やがぽんの順位(" + now + ")"
for i in range(yagapon_rank-1, yagapon_rank+2):
    #extract name and vote
    name = rank_texts[i].text
    vote = r_vote.search(side_nums[i].text).group(0)
    line = str(i+1) + "位 " + name + " " + vote + "票"
    #calculate diff
    diff = int(vote) - int(my_vote)
    if diff >= 0:
        diff = "+" + str(diff)
    else:
        diff = str(diff)
    if name != "やがぽん":
        line = line + "(" + diff + ")"
    #output line
    output += "\n" + line

## add url
string_list = [
    "やがぽんを応援しよう！！",
    "矢上の幼女やがぽんを応援しよう！！",
    "我らの姫やがぽんを応援しよう！！"
]
output += "\n\n" + string_list[random.randint(0, len(string_list)-1)]
output += "\n" + url

# tweet
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
ACCESS_TOKEN = ""
ACCESS_SECRET = ""
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)
api.update_status(output)
