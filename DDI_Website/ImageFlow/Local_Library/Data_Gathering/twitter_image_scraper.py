import tweepy
import pandas as pd
from tqdm import tqdm
import requests
from datetime import datetime
import os
import PIL
from Website_Settings.file_paths import filepaths

saveDirectory = filepaths.file_server_path + "ImageFlow/img/twitter/"

def download_image(url):
    print("Started download")
    response = requests.get(url, stream=True)
    print("response works")

    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    print("Filesize received")

    # get the file name
    file_name = (url.split("/")[-1])
    file_name = (file_name.split("?")[0])

    print("FileName:")
    print(file_name)

    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {file_name}", total=file_size, unit="B",
                    unit_scale=True, unit_divisor=1024)

    with open(file_name, "wb") as f:
        for data in progress.iterable:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))

    image_url = saveDirectory+file_name
    print("opening image")
    print(image_url)

    image = PIL.Image.open(open(image_url, 'rb'))
    width, height = image.size
    global dimension
    dimension=str(width) + " " + str(height)

    return file_name

def scrape_twitter(access_key, access_secret_key, api_key, api_secret_key, start, end, hashtags):
    output_df = []
    path = "/home/webapp/Digital-Democracies-Instititute-Website/DDI_Website/ImageFlow/data/twitter"

    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed  - possible directory already exists" % path)
    else:
        print("Successfully created the directory %s" % path)

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_key, access_secret_key)

    # Create API object
    api = tweepy.API(auth)

    # We are using .Cursor() to search through twitter for the required tweets.
    # The number of tweets can be restricted using .items(number of tweets)

    timeline = tweepy.Cursor(api.search, q=hashtags, since=start, tweet_mode='extended', result_type="recent").items()
    num = 0

    for tweet in timeline:
        num=num+1
        for media in tweet.entities.get("media", [{}]):
            # checks if there is any media-entity
            if media.get("type", None) == "photo":
                # checks if the entity is of the type "photo"
                image_url = media["media_url"]
                print(image_url)
                print(tweet.created_at)
                username = tweet.user.screen_name
                file_name = download_image(image_url)
                date = tweet.created_at
                date_time = str(datetime.timestamp(date))

                # if tweet.place:
                #     country = tweet.place.name
                # else:
                #     country = ""
                # print("Country: " + country)

                print(date_time)
                row = {"file_name": file_name, "imageURL": image_url, "group": hashtags, "username": username,
                       "timestamp": date_time, "country": "", "numComments": 0, "score": 0,
                       "platform": "Twitter", "abs_file_path": saveDirectory + file_name, "dimensions": dimension}

                output_df.append(row)

    print("Total num:" + str(num))
    df = pd.DataFrame(output_df)
    return df



access_key="205910278-5yI9NntPRvcNfg5uKYOkrqXrDDuv0lWUqakacVfp"
access_secret_key = "eFOcxnWjkE6KBhF8wFI96r8DL74E0SHIJFLvdt8WguLoo"

# Monthly cap of 500,000 tweets

api_key = "ujUVWymAGgdyFopRBaAr0Km7U"
api_secret_key = "w1bzf4gNjSXwz39bOj5QcurWSJIhkox29KXidWRJevKm1t5IJW"

#scrape_twitter(access_key, access_secret_key, api_key, api_secret_key, '04/15/2021', '06/22/2021', '#bmw')
