set root=C:\Users\Yashi\Miniconda3

call %root%\Scripts\activate.bat %root%

call python -m social_media_scraper -m id -i "./example-identification.csv" -o "./_temp.csv" -lb 1 -ub 3 -g "C:\Users\Yashi\Documents\geckodriver.exe"

call python -m social_media_scraper -m acc -hi -i "./_temp.csv" -o "./scraping_result.db" -lb 1 -ub 3 -g "C:\Users\Yashi\Documents\geckodriver.exe"

call del /f _temp.csv

pause
