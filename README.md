# M1 Motorway Traffic Data Scraper

## Overview

This project automates the collection of traffic data from the Traffic England website ([trafficengland.com](https://www.trafficengland.com/traffic-report)) for the M1 motorway. It uses Selenium to scrape real-time speed and event information, saving the data to CSV files. The script is scheduled to run at random times throughout the day, covering peak and off-peak hours, to provide a comprehensive dataset for traffic analysis.

## Dependencies

* Python 3.x
* Selenium
* Pandas
* Schedule
* Webdriver for Chrome (ChromeDriver)

## Usage

* The script will automatically scrape data from the Traffic England website and save it to CSV files at scheduled times.
* The data will be collected at random times within the defined time strata, providing a diverse dataset.
* CSV files will be saved in the same directory as the script, with filenames in the format `YYYYMMDD_HHMMSS.csv`.
