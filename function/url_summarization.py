import bs4 as bs
import requests
import re
import nltk
import contractions
import heapq

from bs4 import BeautifulSoup


def search(url: str, status: bool):
    expanded_text = ""
    if status is True:
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
    elif status is False:
        expanded_text = url

    article_text = re.sub(r'\[[0-9]*\]', ' ', expanded_text)
    article_text = re.sub(r'\s+', ' ', article_text)

    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

    sentence_list = nltk.sent_tokenize(article_text)
    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequency = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequency)

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)
    return summary


def text_summarization(summary: str, model, tokenizer, device):
    t5_prepared_text = "summarize: " + summary
    tokenized_text = tokenizer.encode(t5_prepared_text, return_tensors="pt").to(device)
    summary_ids = model.generate(tokenized_text,
                                 num_beams=5,
                                 no_repeat_ngram_size=2,
                                 max_length=10000,
                                 early_stopping=True)

    output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return output


def print_sum(link_search, model, tokenizer, device):
    for link in link_search:
        summary = search(link, True)
        summary = text_summarization(summary, model, tokenizer, device)
        print("link: " + link)
        print("Summary: "+summary)
    print()


def url_sum(model, tokenizer, device, url):
    link_search = [url]
    print_sum(link_search, model, tokenizer, device)


def search_wiki(model, tokenizer, device):
    app_status = True
    link_search = []
    exit_status = False
    word_search = input("What do you want to search?\n(q to quit): ")
    search_replace = word_search.replace(" ", "+")
    url = "https://en.wikipedia.org/w/index.php?title=Special:Search&limit=7&offset=0&ns0=1&search=" + search_replace
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'lxml')

    for find in soup.find_all("div", class_="searchdidyoumean"):
        print(find.text)
        if "No results found for" in find.text:
            print("Please search new one\n")
            exit_status = True
            app_status = False
            break
        status = input("(y/n): ")
        if status == 'y':
            text = find.text.replace("Did you mean: ", "").replace(" ", "+")
            url = "https://en.wikipedia.org/w/index.php?title=Special:Search&limit=7&offset=0&ns0=1&search=" + text
            req = requests.get(url)
            soup = BeautifulSoup(req.text, 'lxml')
            break
        elif status == 'n':
            break

    if exit_status is False:

        for exists in soup.find_all("p", class_="mw-search-exists"):
            print(exists.text)
            print("Do you want to go on this page?")
            status = input("(y/n): ")
            if status == 'y':
                page_url = exists.find("a", href=True)
                link_search.append("https://en.wikipedia.org"+page_url['href'])
                print("Summarize from 1 web page")
                break
            elif status == 'n':
                for find in soup.find_all("li", class_="mw-search-result"):
                    href = find.find('a')
                    link_search.append("https://en.wikipedia.org" + href['href'])
                print("Summarize from 7 web page")
                break

        for find in soup.find_all("p", class_="mw-search-createlink"):
            if "does not exist." in find.text:
                print("The page \"" + word_search + "\" does not exist.")
                print("Please search new one.\n")
                app_status = False
    if app_status is True:
        print_sum(link_search, model, tokenizer, device)
