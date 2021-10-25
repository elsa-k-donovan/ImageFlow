# ImageFlow
🔎 🗺️ Social Media Image Analysis Web App

[![Build Status](http://img.shields.io/travis/badges/badgerbadgerbadger.svg?style=flat-square)](https://travis-ci.org/badges/badgerbadgerbadger)
![Screenshot](imgs/header_screenshot.png)

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Web Scrapers](#web-scrapers)
- [FAQ](#faq)


> This project is written in Python using Tweepy, PostgreSQL, Celery integrated into Django for an easy to use website interface.

## Introduction

<div align='center'><img src="imgs/github_sample_gif.gif" text-align="center" height="400px"></div>

<br />
This app is designed for social media researchers and other investigators who have access to academic API keys for major social media platforms. ImageFlow is useful for those who have to collect large databases of images and need a way to easily view how similar or identical images flow from platform to platform. 
<br /><br />
ImageFlow integrates the data gathering process by using four custom web scrapers: 4plebs (the archive for 4chan - since 4chan threads frequently expire), Facebook, Twitter, and Reddit. After the data gathering phase is complete the resulting image database can be clustered in the Image Analysis page. The user can choose to perform a clustering algorithm which will either cluster their database by similar images or by identical images. When the clustering is complete, the final result will show on the Image Visualization page. This page displays only the images that have been clustered, and shows the timeline of movement across platforms.
<br /><br />
This app is a locally-hosted version of the web-tool developed for the <a href="https://digitaldemocracies.org/"> Digital Democracies Institute </a> at Simon Fraser University. This version requires that the user have enough hardware space for all the images that they desire to download and analyze. 

## Installation
Python 3.6

### Using Docker

1) Download <a href="https://www.docker.com/products/docker-desktop"> Docker for Desktop </a> - restart your computer after installation and make sure it is running before continuing. In Docker Desktop, especially on Macs, please increase the amount of memory available to at least 8GB.

2) Clone this repo to your local machine

3) Open Terminal (Mac) or CMD (Windows) and CD into the local repo.

4) Run docker-compose up to start server

      '''
      docker-compose up 
      '''

5) Go to http://localhost:8000/login/ on your browser to begin.

Now the website is fully functional!

Just register a new user at http://localhost:8000/login/ and enjoy!

## Web Scrapers

There are four social media APIs used in this project:
- CrowdTangle
- 4Plebs
- PushShift
- Twitter

### Limitations

#### Crowdtangle

Posts and /posts/search will max out at 10,000 posts returned. You can ONLY search the PAGES and GROUPS that are in your dashboard.
The time between startDate and endDate must be less than a year. Can only handle 10k posts at a time.

#### Twitter

On this local-version of the ImageFlow web app you are able to search for particular users getting up to the most recent 3200 tweets, search via hashtag in the last 7 days using our non-premium or search the full archive of twitter using the premium twitter account

Once data has been searched for, you can query the data on the query tab and get a CSV file containing the tweets and some other useful fields in relation with them.


## FAQ

**What if nothing is showing up at my localhost URL?**

Try these two links, if one is not working than the other one should: <br />
http://127.0.0.1:8000/ <br />
http://127.0.0.1:8000/login/ <br />


