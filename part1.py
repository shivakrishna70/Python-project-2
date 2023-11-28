import requests
import xml.etree.ElementTree as ET
import pandas as pd
import gzip

URL = (
    "https://www.hackerrank.com/"  # Using hackerrank site to site the data scraping for
)


class SitemapParser:
    def __init__(self, base_url):
        """
        params:
          base_url: url to parse the robots.txt data to retrieve the Sitemap data
        return: None
        """
        self.base_url = base_url
        self.sitemaps = []

    def fetch_robots_txt(self):
        """
        params: None
        return: str
        """
        robots_url = f"{self.base_url}/robots.txt"
        # headers for the authentication purpose of the data
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
        try:
            # getting response of urL with help of requests module.
            response = requests.get(robots_url, headers=headers)
            response.raise_for_status()
            # print(response.text)
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching robots.txt: {e}")
            return None

    def extract_sitemaps(self, robots_content):
        """
        params:
            robots_content: content of the urL data
        return: list of sitemaps urls
        """
        sitemaps = []
        if robots_content:
            # fetching the content of the sitemap for the urL only.
            lines = robots_content.split("\n")
            for line in lines:
                if line.startswith("Sitemap:"):
                    sitemap_url = line.split(": ")[1].strip()
                    sitemaps.append(sitemap_url)
        return sitemaps

    def parse_sitemap(self, sitemap_url):
        """
        params:
          sitemap_urL: url content of the xmL data containing the sitemap for the hackerrank
        return: list of contents urL's of the xmL data for the hackerrank
        """
        try:
            # fetching the content of the urLs data using requests api
            response = requests.get(sitemap_url)
            response.raise_for_status()
            # Decompress the gzip content
            decompressed_content = gzip.decompress(response.content).decode("utf-8")
            # Parse XML content
            root = ET.fromstring(decompressed_content)
            # Extract URLs
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
        params: None
        return: data frame with list of urL's of the hackerrank sitemap xmL's data
        """
        robots_content = self.fetch_robots_txt()
        self.sitemaps = self.extract_sitemaps(robots_content)

        all_urls = []
        for sitemap_url in self.sitemaps:
            urls = self.parse_sitemap(sitemap_url)
            all_urls.extend(urls)

        df = pd.DataFrame(all_urls, columns=["URL"])
        return df
        # return None


# Example usage with a website
website_url = URL
sitemap_parser = SitemapParser(website_url)
result_df = sitemap_parser.parse_all_sitemaps()

# Display the DataFrame
print(result_df)
