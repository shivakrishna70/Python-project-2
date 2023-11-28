from newsapi import NewsApiClient
import pandas as pd


class NewsApi:
    def __init__(self):
        """
        Initialize the NewsApi class with a News API key.

        Parameters:
        - None

        Returns:
        - None
        """
        # Initialize news API with the provided API key
        self.newsapi = NewsApiClient(api_key="a148c40805264d4a9646cd368dd20508")

    def getTopHeadLines(self):
        """
        Retrieve top headlines related to Bitcoin from the News API.

        Parameters:
        - None

        Returns:
        - None
        """
        self.top_headlines = self.newsapi.get_top_headlines(
            q="bitcoin", category="business", language="en", country="us"
        )

    def getAllArticles(self):
        """
        Retrieve all articles related to Bitcoin from specific sources within a date range.

        Parameters:
        - None

        Returns:
        - None
        """
        self.all_articles = self.newsapi.get_everything(
            q="bitcoin",
            sources="bbc-news,the-verge",
            domains="bbc.co.uk,techcrunch.com",
            from_param="2023-10-29",
            to="2023-11-20",
            language="en",
            sort_by="relevancy",
            page=2,
        )

    def getSources(self):
        """
        Retrieve sources providing information about Bitcoin from the News API.

        Parameters:
        - None

        Returns:
        - None
        """
        self.sources = self.newsapi.get_sources()

    def getDatatoDF(self):
        """
        Convert the requested data into a DataFrame.

        Parameters:
        - None

        Returns:
        - pandas.DataFrame: A DataFrame containing information about sources providing Bitcoin-related news.
        """
        # Retrieve data from News API
        self.getTopHeadLines()
        self.getAllArticles()
        self.getSources()

        # Extract sources data
        sources_data = self.sources["sources"]

        # Convert the list of dictionaries into a DataFrame
        df_sources = pd.DataFrame(sources_data)

        return df_sources


# Example usage with NewsApi class
news_api = NewsApi()
news_df = news_api.getDatatoDF()
print(news_df.head())
