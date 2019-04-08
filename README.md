# SocialMediaScraper

## social_media_scraper

> Scraper for twitter, LinkedIn and Xing accounts.

Input data example is in __example.csv__ file.
All Requirements are listed in requirements.txt file, but also [Gecko driver](https://github.com/mozilla/geckodriver/releases) must be in PATH.
### Running application
>python -m social_media_scraper [-h] -m MODE [-i INPUT] [-o OUTPUT] [-lb LOWER_BOUND] [-ub UPPER_BOUND] [-he] [-d] [-g GECKODRIVER] [-s] [-hi] [-aa ACCOUNT_AMOUNT]

#### Settings for application

Common arguments:

  __-h, --help__
  Show this help message and exit

  __-m MODE, --mode MODE__ 
  Scrape user account or match identity by data (pass acc or id respectively)

  __-i INPUT, --input INPUT__
  Input file location

  __-o OUTPUT, --output OUTPUT__
  Output file location

  __-lb LOWER_BOUND, --lower_bound LOWER_BOUND__
  Request frequency lower bound

  __-ub UPPER_BOUND, --upper_bound UPPER_BOUND__
  Request frequency upper bound

  __-he, --headless__
  Run browser in headless mode

  __-g GECKODRIVER, --geckodriver GECKODRIVER__
  Set path for geckodriver

Identity parser arguments:

  __-aa ACCOUNT_AMOUNT, --account_amount ACCOUNT_AMOUNT__
  Amount of accounts to match

Social media parser arguments:
  __-d, --debugging__
  Runs application in debug mode (will log debug logs into console)

  __-g GECKODRIVER, --geckodriver GECKODRIVER__
  Set path for geckodriver

  __-s, --sql__
  Log sql into console

  __-hi, --headless_interface__
  Run app in headless mode, you should specify input and output files if set to true

#### Example command

Account scraping:
> python -m social_media_scraper -m acc

Identification:

> python -m social_media_scraper -m id -i "./example-identification.csv" -o "./result.csv" -lb 1 -ub 3

## company_scraper

> Scraper for scraping google news and kununu pages of companies

Input data exapmple is in __example-company.csv__ file.
Before starting application make sure, that all required packages are installed with command:
> pip install aiohttp lxml newspaper3k yarl

### Running application

__python -m company_scraper__ [-h] __-l__ LANGUAGE __-i__ INPUT __-o__ OUTPUT

#### Arguments:
  __-h, --help__
  Show help message and exit

  __-l LANGUAGE, --language LANGUAGE__
  Set language for news articles ('en' or 'de')

  __-i INPUT, --input INPUT__
  Set input file for processing

  __-o OUTPUT, --output OUTPUT__
  Output file for scraping results

#### Example command:

> python -m company_scraper -l "de" -i "example-company.csv" -o "data.db"