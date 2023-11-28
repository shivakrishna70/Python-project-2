from newsapi import NewsApiClient
import pandas as pd

# pip install newsapi-python


class NewsApi:
    def __init__(self):
        # initialize news api
        self.newsapi = NewsApiClient(api_key="a148c40805264d4a9646cd368dd20508")

    def getTopHeadLines(self):  # used to get the top head lines for bitcoins
        self.top_headlines = self.newsapi.get_top_headlines(
            q="bitcoin", category="business", language="en", country="us"
        )

    def getAllArticles(
        self,
    ):  # used to get the articles related to bitcoins from sources bbc-news, the verge in range 10/21 to 11/01
        self.all_articles = self.newsapi.get_everything(
            q="bitcoin",
            sources="bbc-news,the-verge",
            domains="bbc.co.uk,techcrunch.com",
            from_param="2023-10-21",
            to="2023-11-01",
            language="en",
            sort_by="relevancy",
            page=2,
        )

    def getSources(
        self,
    ):  # get the data for the latest status regarding the bitcoins from bbc news in range of 10/21 to 11/01
        self.sources = self.newsapi.get_sources()

    def getDatatoDF(self):  # converting the requested data into data frame
        self.getTopHeadLines()
        self.getAllArticles()
        self.getSources()

        sources_data = self.sources["sources"]
        # Convert the list of dictionaries into a DataFrame
        df_sources = pd.DataFrame(sources_data)

        return df_sources


news_api = NewsApi()
news_df = news_api.getDatatoDF()
news_df.head()
