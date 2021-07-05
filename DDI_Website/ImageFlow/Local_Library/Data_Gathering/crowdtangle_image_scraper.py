from datetime import datetime
import requests
from minet.crowdtangle import CrowdTangleAPIClient
import os
from tqdm import tqdm
import pandas as pd
import PIL
from Website_Settings.file_paths import filepaths

saveDirectory = filepaths.file_server_path + "ImageFlow/img/facebook/"


# Restrictions:
# /posts and /posts/search will max out at 10,000 posts returned.
# count = 100, offset=100 (shows post 101-200)
# you can ONLY search the PAGES and GROUPS that are in your dashboard.
# The time between startDate and endDate must be less than a year.

# Only 10k posts at a time

# Everyone in the same dashboard will have the same API token

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


def scrape_facebook(api_token, startDate_old, endDate_old):
    output_df = []
    base_url = "https://api.crowdtangle.com/posts?token=" + api_token
    url = "https://api.crowdtangle.com/posts?token=" + api_token + "&types=photo"
    path = "/home/webapp/Digital-Democracies-Instititute-Website/DDI_Website/ImageFlow/data/facebook"

    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed  - possible directory already exists" % path)
    else:
        print("Successfully created the directory %s" % path)

    current_page = 0

    # Date formats for CrowdTangle API should be: yyyy-mm-dd
    datetimeobject = datetime.strptime(startDate_old, '%m/%d/%Y')
    startDate = datetimeobject.strftime('%Y-%m-%d')

    datetimeobject = datetime.strptime(endDate_old, '%m/%d/%Y')
    endDate = datetimeobject.strftime('%Y-%m-%d')

    url_scrape = url + "&startDate=" + startDate + "&endDate=" + endDate
    print(url_scrape)

    client = CrowdTangleAPIClient(token=api_token)

    count = 0

    posts = client.posts(type='photo', start_date=startDate, end_date=endDate, sort_by='DATE')
    for post in posts:
        # print(post)
        count += 1
        if post['type'] == 'photo':
            media = (post['media'])
            date_time = post['datetime']
            datetimeobject = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
            date_time = int(datetimeobject.timestamp())

            media = str(media)

            media = media.split()
            isURL = False

            for i in media:
                if isURL:
                    # print(i)
                    image_url = i
                    break
                if "url" in i:
                    isURL = True

            username = post['account_name']
            score = post['score']
            group_type = post['account_type']
            country = post['account_page_admin_top_country']

            try:
                # download image file to database folder
                # print(image_url)
                image_url = image_url.strip('\',')
                file_name = download_image(image_url)

                print(dimension)

                print("Successfully downloaded image.")
                try:
                    # TODO: Not sure how to add filename at the moment
                    row = {"file_name": file_name, "imageURL": image_url, "group": username, "username": username,
                           "timestamp": date_time, "country": country, "numComments": 0, "score": score,
                           "platform": "Facebook", "abs_file_path": saveDirectory + file_name, "dimensions": dimension}

                    output_df.append(row)

                except Exception as ex2:
                    print("Unable to add row to dataframe")

            except Exception as ex:
                print("Unable to download image. No data collected.")

    df = pd.DataFrame(output_df)
    return df


# scrape_facebook('GUexChh20anhPIEc8pkTzy2OhVzcTcGtwX97DxQA', '04/15/2021', '10/25/2021')
