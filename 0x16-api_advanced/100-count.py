#!/usr/bin/python3
""" Count it! """
import requests
import json
import re

def count_words(subreddit, word_list, after=None, count_dict=None):
    if count_dict is None:
        count_dict = {}
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"limit": "100"}
    if after is not None:
        params["after"] = after
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)
    if response.status_code != 200:
        return
    data = json.loads(response.text)
    posts = data["data"]["children"]
    for post in posts:
        title = post["data"]["title"]
        for word in word_list:
            if word.lower() in re.findall(r'\b[a-z]+\b', title.lower()):
                if word.lower() in count_dict:
                    count_dict[word.lower()] += 1
                else:
                    count_dict[word.lower()] = 1
    if len(posts) == 100:
        count_words(subreddit, word_list, after=posts[-1]["data"]["name"], count_dict=count_dict)
    else:
        sorted_counts = sorted(count_dict.items(), key=lambda x: (-x[1], x[0]))
        for count in sorted_counts:
            print(f"{count[0]}: {count[1]}")

