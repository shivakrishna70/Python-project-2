from typing import ParamSpecKwargs

# You code here (Please add comments in the code):

import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd


class Scholarly:
    def __init__(self):
        pass

    def get_soup(self, url):
        """
        params1: url (contains the url of google scholar page)
        return: soup (fetching the url page data and then further converted to html parser)
        """
        # headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        }
        try:
            # requesting for data using requests with url and headers for authentication
            data = requests.get(url, headers)
            # print(f"Extracted the data with response as {data.status_code}")
            if data.status_code != 200:
                raise Exception("Failed to fetch data")
        except Exception as ex:
            print(
                f"Exception occurred as {data.text} with status_code {data.status_code}"
            )
            return None
        soup = BeautifulSoup(data.content)
        return soup

    def get_title(self, title):
        """
        params1: soup_api with fetched title of article
        return: string format of text title of article
        """
        return str(title.find("a").text)

    def get_abstract_url(self, title):
        """
        params1: soup_api with fetched title of article
        return: string format of url for title of article
        """
        return str(title.find("a").get("href"))

    def get_article_info(self, article):
        """
        params1: soup_api with fetched article info
        return: tuples containing author, year, and published info
        """
        # using regular expressions, fetched year from article
        year = int(re.search(r"\d+", article.text).group())
        # performing some string operations, fetched required results
        article = str(article.text).replace("\xa0", "")
        article = article.split("-")
        published = article[-1].strip()
        author = article[0].strip()
        return author, year, published

    def get_tags(self, soup):
        """
        params1: soup_api with fetched url and parsed data
        return: list of article info, such as titles, authors, year, published, abstract
        """
        # fetched titles and authors of article using findAll by mentioning some tags
        all_titles = soup.findAll("h3", attrs={"class": "gs_rt"})
        all_authors = soup.findAll("div", attrs={"class": "gs_a"})
        all_abstracts = soup.findAll("div", attrs={"class": "gs_rs"})

        authors, year, published = [], [], []

        titles = [self.get_title(title) for title in all_titles]
        abs_url = [self.get_abstract_url(title) for title in all_titles]
        abstract = [self.get_abstract(abstr) for abstr in all_abstracts]

        for author in all_authors:
            auth, yr, publs = self.get_article_info(author)
            authors.append(auth)
            year.append(yr)
            published.append(publs)

        return titles, authors, year, published, abstract, abs_url

    def get_abstract(self, abstr):
        """
        params1: soup_Api with fetched abstract of article
        return: string format of article abstract by fetching its text
        """
        return str(abstr.text).replace("\n", "")

    def fetch_web_data(self, records):
        """
        params1(records): number of articles, needs to be fetched
        return: dataframe containing total N number of articles.
        """
        year_st, year_end = 2012, 2022
        columns_google = [
            "Title",
            "Author",
            "Year",
            "Published",
            "Abstract",
            "Abstract_UrL",
        ]
        # fetching for 1000 articles
        titles, authors, years, published, abstract, abs_url = [], [], [], [], [], []
        final_data = []
        print("***** BEFORE FETCHING *********")
        # records = 100 # no of articles
        for i in range(0, records, 10):
            url = f"https://scholar.google.com/scholar?start={i}&q=information+retrieval&hl=en&as_sdt=0,44&as_ylo={year_st}&as_yhi={year_end}&as_vis=1"
            soup = self.get_soup(url)
            if soup is None:
                print(f"Data Not Fetched.... for {i} article page")
                continue
            # titles, authors, year, published, abstract, abs_url
            a, b, c, d, e, f = self.get_tags(soup)
            titles.extend(a)
            authors.extend(b)
            years.extend(c)
            published.extend(d)
            abstract.extend(e)
            abs_url.extend(f)
            print(f"******* fetched {(i+10)} articles *********")
            # keeping time to sleep for 5 seconds, so that, server may not crash for frequent multiple requests.
            time.sleep(5)

        for i in range(records):
            final_data.append(
                [titles[i], authors[i], years[i], published[i], abstract[i], abs_url[i]]
            )

        print("******* AFTER FETCHING ********")
        df = pd.DataFrame(final_data, columns=columns_google)
        print(f"Number of records: {df.shape[0]}")
        return df


scholarly = Scholarly()
df = scholarly.fetch_web_data(int(input("Enter num of articles: ")))
print(f"dimensions of articles: {df.shape}")
df.head()
