import requests
import contractions
import re
import bs4 as bs
import nltk
import numpy as np
import pandas as pd


def increase_word(url):
    df = pd.read_csv('all_function/word/list_of_word.csv')
    load_list = df['All_Word'].tolist()

    scraped_data = requests.get(url)
    parsed_article = bs.BeautifulSoup(scraped_data.text, 'lxml')
    paragraphs = parsed_article.find_all('p')

    article_text = ""

    for p in paragraphs:
        article_text += p.text

    expanded = []
    for word in article_text.split():
        expanded.append(contractions.fix(word))

    expanded_text = ' '.join(expanded)
    article_text = re.sub(r'\[[0-9]*\]', ' ', expanded_text)
    article_text = re.sub(r'\s+', ' ', article_text)

    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

    sentence_list = nltk.sent_tokenize(formatted_article_text)
    stopwords = nltk.corpus.stopwords.words('english')
    all_word = ' '.join(sentence_list).split()
    list_word = []
    for word in all_word:
        word = word.lower()
        if word not in stopwords:
            if word not in list_word:
                list_word.append(word)

    for word in list_word:
        word = word.lower()
        if word not in stopwords:
            if word not in load_list:
                load_list.append(word)

    load_list = np.array(load_list)
    load_list = pd.DataFrame(data=load_list)
    load_list.columns = ['All_Word']
    load_list.to_csv('all_function/word/list_of_word.csv', index=False)
