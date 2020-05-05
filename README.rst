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
    2. requests



Running the spider
==================

Open Your project folder in terminal and write command::

    $ scrapy crawl people
    
Scrapy will automaticaly save your data to ``people_items.csv`` file in root of a project.

**NOTICE!!!** Each crawling will rewrite the csv file.
