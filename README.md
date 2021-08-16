# ImageFlow
🔎 🗺️ Social Media Image Analysis Web App

[![Build Status](http://img.shields.io/travis/badges/badgerbadgerbadger.svg?style=flat-square)](https://travis-ci.org/badges/badgerbadgerbadger)

## Table of Contents

- [Installation](#installation)
- [Web Scrapers](#web)
- [FAQ](#faq)


> This project is written in Python using Tweepy, PostgreSQL, Celery integrated into Django for an easy to use website interface.

On this local-version of the ImageFlow web app you are able to search for particular users getting up to the most recent 3200 tweets, search via hashtag in the last 7 days using our non-premium or search the full archive of twitter using the premium twitter account

Once data has been searched for, you can query the data on the query tab and get a CSV file containing the tweets and some other useful fields in relation with them.

## Installation
Python 3.6

### Setup

> Update and install this package first


To run this server on your local host:

1) git clone this repo into your text editor

2) On the front page of this repo, copy the requirements.txt file into your project and download it

      a) need to download apache2 for modwsgi, 
        
        brew install postgresql
        brew install apache2
        pip install -r requirements.txt 
               
3) Create a 'frontend_config.py' file for our settings.py file in Website_Settings, of form

       Django = {
           "Key": '',
       }

       PostgreSQL = {
           "UserName": "",
           "Password": "",
           "Name": "",
           "Host": "",
           "Port": ,
       }
        
4) Go into the DDI directory

        cd DDI_Website

5) Then once the above steps are completed, you now run in order in the terminal:

        python manage.py makemigrations
        python manage.py migrate
        python manage.py runserver // For just the regular server (for testing purposes)

6) Then create a new terminal instance while still in DDI_Website folder

        if windows 10:
            pip install gevent 
            celery -A Website_Settings worker -l info -P gevent
        if macOS:
            celery -A Website_Settings worker -l info

This will let you run your tasks in the background using Celery

Now the website is fully functional!

Just register a new user and enjoy :)

## Web Scrapers

There are four social media APIs used in this project:
- CrowdTangle
- 4Plebs Archive 
- PushShift
- Twitter

## FAQ


