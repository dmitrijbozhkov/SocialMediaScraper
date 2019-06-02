# SocialMediaScraper

## social_media_scraper

> Scraper for twitter, LinkedIn and Xing accounts.

Input data example is in __example.csv__ file.
All Requirements are listed in requirements.txt file, but also [Gecko driver](https://github.com/mozilla/geckodriver/releases) must be in PATH.
### Running application
>python -m social_media_scraper [-h] -m MODE [-i INPUT] [-o OUTPUT] [-lb LOWER_BOUND] [-ub UPPER_BOUND] [-g GECKODRIVER] [-d] [-s] [-int]

#### Arguments
  __-h, --help__
  show this help message and exit

  __-m MODE, --mode MODE__ 
  Scrape user account, match identity by data or both (pass acc, id or full respectively)

  __-i INPUT, --input INPUT__
  Input file location

  __-o OUTPUT, --output OUTPUT__
  Output file location

  __-lb LOWER_BOUND, --lower_bound LOWER_BOUND__
  Request frequency lower bound

  __-ub UPPER_BOUND, --upper_bound UPPER_BOUND__
  Request frequency upper bound

  __-g GECKODRIVER, --geckodriver GECKODRIVER__
  Set path for geckodriver

  __-d, --debugging__
  Runs application in debug mode (will log debug logs into console)
  
  __-s, --sql__
  log sql into console

#### Example command

> python -m social_media_scraper -m full -i "./example-identification.csv" -o "./output.db" -lb 1 -ub 3 -d -s -g "/path/to/driver/geckodriver.exe"

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