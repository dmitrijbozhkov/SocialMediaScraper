""" Google news page constants """

GOOGLE_NEWS_URL = "https://news.google.com"
GOOGLE_NEWS_EN_SEARCH = "/search?q={}&hl=en-GB&gl=GB&ceid=GB:en"
GOOGLE_NEWS_DE_SEARCH = "/search?q={}&hl=de&gl=DE&ceid=DE:de"
# Selectors
ARTICLE_LINK = "//article/h4/a"
# Headers
BROWSER_HEADERS = {
    "Accept": "text/html",
    "Accept-Encoding": "gzip",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/72.0.3626.121 Chrome/72.0.3626.121 Safari/537.36",
    "Accept-Charset": "utf-8",
    "Connection": "close"
}