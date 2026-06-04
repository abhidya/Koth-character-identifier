import json as json
import re
import string
import requests
from bs4 import BeautifulSoup
try:
    from robobrowser import RoboBrowser
except ImportError:
    RoboBrowser = None


def strip_links(text):
    try:
        link_regex = re.compile(r'((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
        links = re.findall(link_regex, str(text))
        for link in links:
            text = text.replace(link[0], ', ')
        return text
    except:
        return text


def strip_all_entities(text):
  #  print(text)
    entity_prefixes = ['@', '#']
    for separator in string.punctuation:
        if separator not in entity_prefixes:
            text = text.replace(separator, ' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)


def get_tweets(handle, max_position=None):
    if RoboBrowser is None:
        return "Twitter Search Error: RoboBrowser is not installed"

    session = requests.Session()
    browser = RoboBrowser(session=session, parser="lxml")
    url = "https://twitter.com/i/profiles/show/" + handle + "/timeline/tweets?include_available_features=false&include_entities=false&reset_error_state=false"
    if max_position != None:
        url = url + "&" + "max_position=" + max_position
    try:
        browser.open(url)
        result = json.loads(browser.response.content)
        min_position = result['min_position']

    except ValueError:
        return "Twitter Search Error: Is the username correct"
    soup = BeautifulSoup(result['items_html'], 'lxml')
    tweets = soup.find_all("p", {"class": "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"})
    return min_position, tweets


def clean_tweets(tweets):
    return [strip_all_entities(strip_links(i.text)) for i in tweets]


def hitting_twitter(handle):
    if handle.lower() in {"demo", "offline", "fixture"}:
        return [
            "I tell you what, propane and lawn work make a fine afternoon.",
            "That school dance joke was funny enough for extra snacks.",
            "My Spanish class essay proves I am a genius teacher.",
            "The government alien conspiracy fits in my pocket.",
        ]

    first_page = get_tweets(handle)
    if isinstance(first_page, str):
        return first_page

    min_position, tweets = first_page
    for i in range(0, 6):
        min_position1, links1 = get_tweets(handle, min_position)
        tweets = tweets + links1
        if min_position1 is None:
            break
        min_position = min_position1

    if tweets == "Twitter Search Error: Is the username correct":
        return tweets
    tweets = clean_tweets(tweets)
    return tweets
