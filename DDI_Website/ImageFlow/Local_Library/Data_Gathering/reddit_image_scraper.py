from datetime import datetime

from psaw import PushshiftAPI
import wget
import os
import subprocess
import pandas as pd
import time
import datetime as dt
import requests
from tqdm import tqdm
import PIL
from Website_Settings.file_paths import filepaths

saveDirectory = filepaths.file_server_path + "ImageFlow/img/reddit/"
#count_num = 0

# Easy conversion for date to UNIX timestamps here: https://www.unixtimestamp.com/index.php

# NEW RATE LIMIT: 1 REQUEST per Second
##########################################
##########################################


def download_image(url):
    print("Started download")
    response = requests.get(url, stream=True)
    print("response works")

    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    print("Filesize received")

    # get the file name
    file_name = (url.split("/")[-1])
    #print("FileName:")
    #print(file_name)

    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {file_name}", total=file_size, unit="B",
                    unit_scale=True, unit_divisor=1024)

    print("Progress bar done")
    #print(saveDirectory)
    #print(saveDirectory + file_name)

    with open(saveDirectory + file_name, "wb") as f:
        for data in progress.iterable:
            # write data read to the file
            print(saveDirectory)
            print(saveDirectory + file_name)
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))

    image_url = saveDirectory+file_name
    print("opening image")
    #print(image_url)


    image = PIL.Image.open(open(image_url, 'rb'))
    width, height = image.size
    global dimension
    dimension=str(width) + " " + str(height)
    
    return file_name

def scrape_reddit(sub_list, startDate, endDate):
    count_num = 0
    start_time = time.time()

    #path = "/home/webapp/Digital-Democracies-Instititute-Website/DDI_Website/ImageFlow/data/reddit"

    # try:
    #     os.mkdir(path)
    # except OSError:
    #     print("Creation of the directory %s failed" % path)
    # else:
    #     print("Successfully created the day directory %s " % path)

    # Connect to PushShift API
    try:
        api = PushshiftAPI()
    except Exception as ex1:
        print("unable to connect to PushShift")

    output = []
    output_df = []

    #local_path = os.getcwd()
    #local_path = ""

    # USER INPUT SUBREDDIT LIST AND START AND END DATE CONVERTED TO TIMESTAMP
    #sub_list = ['canada', 'canadaleft']

    after =int(time.mktime(dt.datetime.strptime(startDate, "%m/%d/%Y").timetuple()))
    before =int(time.mktime(dt.datetime.strptime(endDate, "%m/%d/%Y").timetuple()))
    print(before)
    print(after)
    # after = '1567296000' #Sept 1, 2019
    # before = '1575158340' #Nov 30, 2019


    curr_date = str(datetime.date(datetime.now()))
    curr_date = curr_date.replace('-','')

    brokenImageLinks = 0
    counter = 0

    for subreddit in sub_list:
        print("Scraping images in "+str(subreddit)+" begins...")
        print("...")

        print(subreddit)

        try:
            #Add a limit here if you would like
            meme_list = list(api.search_submissions(subreddit=str(subreddit), filter=['url', 'author', 'created_utc', 'score', 'num_comments'], after=str(after), before=str(before)))
            count_num = count_num + 1
            #print(meme_list)

        except Exception as search_Except:
            print("unable to make query through pushShift")


        for meme in meme_list:
            #scrapes jpg, gif, and png
            if (str(meme.url).endswith('.jpg') or str(meme.url).endswith('.gif') or str(meme.url).endswith('.jpeg') or str(meme.url).endswith('.png')):

                counter += 1

                #and not str(meme.url).startswith('https://i.imgflip.com')
                #print(meme.url)

                redditScore = str(meme.score)
                numCmts = str(meme.num_comments)
                redditDate = str(meme.created_utc)

                try:
                    # file_name = subreddit + redditDate
                    file_name = download_image(meme.url)

                    # ////PUT IN SEPARATE FUNCTION /////
                    unixTime = meme.created_utc
                    timestamp = str(unixTime)
                    print(dimension)

                    # redditScore and NumComments are added as strings not int
                    try:
                        row = {"file_name": file_name, "imageURL": meme.url, "group": subreddit, "username": meme.author, "timestamp": timestamp, "country": "", "numComments": numCmts, "score": redditScore, "platform": "Reddit", "abs_file_path": saveDirectory + file_name, "dimensions": dimension}

                        output_df.append(row)
                        #print(meme.url)

                    except Exception as ex1:
                        print("row creation failed")


                except Exception as ex:
                    print("Image URL Broken. Could not download.")

                print("\n")
        
        
        print("Requests made: " + str(count_num))


    #create DF
    df = pd.DataFrame(output_df)
    df.to_csv(filepaths.file_server_path + "test_reddit.csv")

    print("...")
    print("Total Broken Image Links: "+str(brokenImageLinks))
    print("Total attempted image posts: "+str(counter))
    print("--- %s seconds ---" % (time.time() - start_time))
    print("--- %s seconds ---" % round(time.time() - start_time, 2))

    return df


#scrape_reddit(['gaming','canada' ], '08/25/2020', '08/27/2020')
