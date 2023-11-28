import requests
import xml.etree.ElementTree as ET
import pandas as pd
import gzip

URL = "https://www.hackerrank.com/"


class SitemapParser:
    def __init__(self, base_url):
        """
        Initialize the SitemapParser with a base URL.

        Parameters:
        - base_url (str): The base URL used to parse the robots.txt data to retrieve Sitemap data.

        Returns:
        - None
        """
        self.base_url = base_url
        self.sitemaps = []

    def fetch_robots_txt(self):
        """
        Fetch the content of the robots.txt file for the specified URL.

        Returns:
        - str: The content of the robots.txt file.
        """
        robots_url = f"{self.base_url}/robots.txt"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
        try:
            response = requests.get(robots_url, headers=headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching robots.txt: {e}")
            return None

    def extract_sitemaps(self, robots_content):
        """
        Extract sitemap URLs from the content of robots.txt.

        Parameters:
        - robots_content (str): The content of the robots.txt file.

        Returns:
        - list: A list of sitemap URLs.
        """
        sitemaps = []
        if robots_content:
            lines = robots_content.split("\n")
            for line in lines:
                if line.startswith("Sitemap:"):
                    sitemap_url = line.split(": ")[1].strip()
                    sitemaps.append(sitemap_url)
        return sitemaps

    def parse_sitemap(self, sitemap_url):
        """
        Parse the sitemap XML content for a given sitemap URL.

        Parameters:
        - sitemap_url (str): The URL of the sitemap XML.

        Returns:
        - list: A list of URLs extracted from the sitemap XML.
        """
        try:
            response = requests.get(sitemap_url)
            response.raise_for_status()
            decompressed_content = gzip.decompress(response.content).decode("utf-8")
            root = ET.fromstring(decompressed_content)
            urls = [
                elem.text
                for elem in root.findall(
                    ".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"
                )
            ]
            return urls
        except requests.exceptions.RequestException as e:
            print(f"Error parsing sitemap: {e}")
            return []

    def parse_all_sitemaps(self):
        """
        Parse all sitemaps for the specified base URL and return the result in a DataFrame.

        Returns:
        - pandas.DataFrame: A DataFrame containing URLs from all parsed sitemaps.
        """
        robots_content = self.fetch_robots_txt()
        self.sitemaps = self.extract_sitemaps(robots_content)

        all_urls = []
        for sitemap_url in self.sitemaps:
            urls = self.parse_sitemap(sitemap_url)
            all_urls.extend(urls)

        df = pd.DataFrame(all_urls, columns=["URL"])
        return df


# Example usage with a website
website_url = URL
sitemap_parser = SitemapParser(website_url)
result_df = sitemap_parser.parse_all_sitemaps()

# Display the DataFrame
print(result_df)
