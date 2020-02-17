set root=/path/to/anaconda/folder/

call %root%\Scripts\activate.bat %root%

call python -m social_media_scraper -m full -i "./example-identification.csv" -o "./output.db" -lb 1 -ub 3 -d -s -tp "/path/to/firefox/profile/folder/" -g "/path/to/driver/geckodriver.exe"

pause
