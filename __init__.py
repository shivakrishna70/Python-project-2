from part1 import *
from part2 import *
from part3 import *


class Main:
    def __init__(self):
        pass

    def _execute_(self):
        # part1
        sitemap_parser = SitemapParser("https://www.hackerrank.com/")
        result_df = sitemap_parser.parse_all_sitemaps()

        # part2
        news_api = NewsApi()
        news_df = news_api.getDatatoDF()

        # part3
        scholarly = Scholarly()
        df = scholarly.fetch_web_data(int(input("Enter num of articles: ")))


if __name__ == "__main__":
    Main()._execute_()
