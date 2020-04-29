Overview
========
This is Scrapy project to scrape people bio from https://www.morganlewis.com/our-people and save data to a CSV file.

Installation
============
Just copy repository to your computer

Requirements
============
Python pakages::

    1. scrapy
    2. scrapy-splash

Configuration
=============
Before starting crawling

1. Change the Splash server address to ``settings.py`` of your Scrapy project
   like this::

      SPLASH_URL = 'http://192.168.59.103:8050'
      
   or leave it::
      
      SPLASH_URL = 'http://localhost:8050'
      
2. Run a Splash instance in your project folder::

    $ docker run -p 8050:8050 scrapinghub/splash

Running the spider
==================

Open Your project folder in terminal and write command::

    $ scrapy crawl people
    
Scrapy will automaticaly save your data to ``people_items.csv`` file in root of a project.

**NOTICE!!!** Each crawling will rewrite the csv file.
