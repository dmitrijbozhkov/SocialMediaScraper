# SocialMediaScraper

## social_media_scraper

> Scraper for twitter, LinkedIn and Xing accounts.

Input data example is in __example.csv__ file.
All Requirements are listed in requirements.txt file, but also [Gecko driver](https://github.com/mozilla/geckodriver/releases) must be in PATH.
#### Running application
> python -m social_media_scraper

## company_scraper

> Scraper for scraping google news and kununu pages of companies

Input data exapmple is in __example-company.csv__ file.
Before starting application make sure, that all required packages are installed with command:
> pip install aiohttp lxml newspaper3k yarl

### Running application

__python -m company_scraper__ [-h] __-l__ LANGUAGE __-i__ INPUT __-ok__ OUTPUT_KUNUNU __-on__ OUTPUT_GOOGLE_NEWS

#### Arguments:
  __-h, --help__            
  Show help message and exit

  __-l LANGUAGE, --language LANGUAGE__
  Set language for news articles ('en' or 'de')

  __-i INPUT, --input INPUT__
  Set input file for processing

  __-ok OUTPUT_KUNUNU, --output_kununu OUTPUT_KUNUNU__
  Output file for kununu

  __-on OUTPUT_GOOGLE_NEWS, --output_google_news OUTPUT_GOOGLE_NEWS__
  Output file for google news

#### Example command:

> python -m company_scraper -i "./example-company.csv" -ok "kununu.csv" -on "google.csv" -l "de"