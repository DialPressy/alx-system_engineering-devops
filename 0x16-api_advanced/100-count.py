#!/usr/bin/python3
""" Count it! """

from collections import defaultdict
from requests import get

REDDIT = "https://www.reddit.com/"
HEADERS = {'User-Agent': 'esw1229/0.0.1'}

def count_words(subreddit, word_list, after=None, word_dict=None):
    if word_dict is None:
        word_dict = defaultdict(int)
        for word in word_list:
            word_dict[word] = 0

    while after is not None:
        params = {'limit': 100, 'after': after}
        url = REDDIT + f"r/{subreddit}/hot/.json"
        response = get(url, headers=HEADERS, params=params, allow_redirects=False)

        if response.status_code != 200:
            print(f"Error {response.status_code} retrieving posts for subreddit {subreddit}")
            return None

        try:
            data = response.json()['data']
            after = data.get('after')
            children = data.get('children')
            for child in children:
                title = child['data']['title']
                words = title.lower().split()
                for word in word_list:
                    word_dict[word] += words.count(word.lower())
        except (ValueError, KeyError, AttributeError) as e:
            print(f"Error processing response: {e}")
            return None

    word_list = [[key, value] for key, value in word_dict.items()]
    word_list = sorted(word_list, key=lambda x: (-x[1], x[0]))
    for word, count in word
