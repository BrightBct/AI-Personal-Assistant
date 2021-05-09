import requests

from bs4 import BeautifulSoup
from summarization.sum_function import search as search_summary
from summarization.sum_function import text_summarization


def print_sum(link_search, model, tokenizer, device):
    for link in link_search:
        summary = search_summary(link, True)
        summary = text_summarization(summary, model, tokenizer, device)
        print("link: " + link)
        print("Summary: "+summary)
    print()


def url_sum(model, tokenizer, device):
    link_search = []
    url = input("Url: ")
    link_search.append(url)
    print_sum(link_search, model, tokenizer, device)


def search_wiki(model, tokenizer, device):
    app_status = True
    link_search = []
    exit_status = False
    search = input("What do you want to search?\n(q to quit): ")
    search_replace = search.replace(" ", "+")
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
                print("The page \""+search+"\" does not exist.")
                print("Please search new one.\n")
                app_status = False
    if app_status is True:
        print_sum(link_search, model, tokenizer, device)
