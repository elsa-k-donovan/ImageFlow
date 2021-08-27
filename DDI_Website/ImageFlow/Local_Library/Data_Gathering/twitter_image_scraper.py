import tweepy
import pandas as pd
from tqdm import tqdm
import requests
from datetime import datetime
import datetime as dt
import time
import os
import PIL
import math
from Website_Settings.file_paths import filepaths
try:
    import Image
except ImportError:
    from PIL import Image

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
    
    #TODO: Make sure this only executes after download is complete. 
    #time.sleep(5)

    with open(saveDirectory + file_name, "wb") as f:
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

#def scrape_twitter(access_key, access_secret_key, api_key, api_secret_key, start, end, hashtags):
def scrape_twitter(api_key, api_secret_key, start, end, hashtags):

    start_time = time.time()

    output_df = []
    # path = "/home/webapp/Digital-Democracies-Instititute-Website/DDI_Website/ImageFlow/data/twitter"

    # try:
    #     os.mkdir(path)
    # except OSError:
    #     print("Creation of the directory %s failed  - possible directory already exists" % path)
    # else:
    #     print("Successfully created the directory %s" % path)

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(api_key, api_secret_key)

    #TODO: Do I need this?
    #auth.set_access_token(access_key, access_secret_key)

    # Create API object
    api = tweepy.API(auth)

    # We are using .Cursor() to search through twitter for the required tweets.
    # The number of tweets can be restricted using .items(number of tweets)
    start = dt.datetime.strptime(start, '%m/%d/%Y').strftime('%Y-%m-%d')
    end = dt.datetime.strptime(end, '%m/%d/%Y').strftime('%Y-%m-%d')

    date_since_pro = start.replace('-','') + str('0000')
    date_until_pro = end.replace('-','') + str('0000')

    print("DATESSS")
    print(date_since_pro)
    print(date_until_pro)

    photo_tweets = 0

    #standard API
    timeline = tweepy.Cursor(api.search_tweets, q=hashtags, until=end).items()

    #premium or Acadmic API
    #timeline = tweepy.Cursor(api.search_full_archive, environment_name='**ENV NAME FROM API**', query=hashtags, fromDate=date_since_pro, toDate=date_until_pro).items()

    print(timeline)
    num = 0

    for tweet in timeline:
        #print(tweet)
        num=num+1
        for media in tweet.entities.get("media", [{}]):
            # checks if there is any media-entity
            if media.get("type", None) == "photo":
                # checks if the entity is of the type "photo"
                photo_tweets = photo_tweets + 1
                image_url = media["media_url"]
                print(image_url)
                print(tweet.created_at)
                username = tweet.user.screen_name
                file_name = download_image(image_url)

                date = tweet.created_at
                print("DATE " + str(date))
                date_time = datetime.timestamp(date)
                date_time = str(int(date_time))


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

    print("Total num of tweets analyzed: " + str(num))
    print("Total num of tweets with photos: " + str(photo_tweets))
    df = pd.DataFrame(output_df)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("--- %s seconds ---" % round(time.time() - start_time, 2))

    return df

