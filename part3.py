import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd


class Scholarly:
    def __init__(self):
        """
        Initialize the Scholarly class.

        This class provides methods to fetch and parse information from Google Scholar articles.

        Parameters:
        - None

        Returns:
        - None
        """
        pass

    def get_soup(self, url):
        """
        Retrieve and parse HTML content from a given URL.

        Parameters:
        - url (str): The URL of the page to fetch.

        Returns:
        - BeautifulSoup: The parsed HTML content.
        """
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        }
        try:
            data = requests.get(url, headers)
            if data.status_code != 200:
                raise Exception("Failed to fetch data")
        except Exception as ex:
            print(
                f"Exception occurred: {data.text} with status_code {data.status_code}"
            )
            return None
        soup = BeautifulSoup(data.content, "html.parser")
        return soup

    def get_title(self, title):
        """
        Extract the title of an article from the provided BeautifulSoup object.

        Parameters:
        - title (BeautifulSoup): The BeautifulSoup object representing the title of an article.

        Returns:
        - str: The text title of the article.
        """
        return str(title.find("a").text)

    def get_abstract_url(self, title):
        """
        Extract the URL for the title of an article from the provided BeautifulSoup object.

        Parameters:
        - title (BeautifulSoup): The BeautifulSoup object representing the title of an article.

        Returns:
        - str: The URL for the title of the article.
        """
        return str(title.find("a").get("href"))

    def get_article_info(self, article):
        """
        Extract author, year, and published information from the provided BeautifulSoup object.

        Parameters:
        - article (BeautifulSoup): The BeautifulSoup object representing an article.

        Returns:
        - tuple: A tuple containing author, year, and published information.
        """
        year = int(re.search(r"\d+", article.text).group())
        article = str(article.text).replace("\xa0", "")
        article = article.split("-")
        published = article[-1].strip()
        author = article[0].strip()
        return author, year, published

    def get_tags(self, soup):
        """
        Extract information from various tags in the provided BeautifulSoup object.

        Parameters:
        - soup (BeautifulSoup): The BeautifulSoup object representing the page content.

        Returns:
        - tuple: A tuple containing lists of titles, authors, years, published, abstracts, and abstract URLs.
        """
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
        Extract the text of an article abstract from the provided BeautifulSoup object.

        Parameters:
        - abstr (BeautifulSoup): The BeautifulSoup object representing the abstract of an article.

        Returns:
        - str: The text of the article abstract.
        """
        return str(abstr.text).replace("\n", "")

    def fetch_web_data(self, records):
        """
        Fetch web data for a specified number of articles and convert it into a DataFrame.

        Parameters:
        - records (int): The number of articles to fetch.

        Returns:
        - pandas.DataFrame: A DataFrame containing information about the fetched articles.
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
        titles, authors, years, published, abstract, abs_url = [], [], [], [], [], []
        final_data = []

        for i in range(0, records, 10):
            url = f"https://scholar.google.com/scholar?start={i}&q=information+retrieval&hl=en&as_sdt=0,44&as_ylo={year_st}&as_yhi={year_end}&as_vis=1"
            soup = self.get_soup(url)
            if soup is None:
                print(f"Data Not Fetched for {i} article page")
                continue

            a, b, c, d, e, f = self.get_tags(soup)
            titles.extend(a)
            authors.extend(b)
            years.extend(c)
            published.extend(d)
            abstract.extend(e)
            abs_url.extend(f)
            print(f"Fetched {i + 10} articles")
            time.sleep(5)

        for i in range(records):
            final_data.append(
                [titles[i], authors[i], years[i], published[i], abstract[i], abs_url[i]]
            )

        df = pd.DataFrame(final_data, columns=columns_google)
        print(f"Number of records: {df.shape[0]}")
        return df


# Example usage with Scholarly class
scholarly = Scholarly()
df = scholarly.fetch_web_data(int(input("Enter num of articles: ")))
print(f"Dimensions of articles: {df.shape}")
df.head()
