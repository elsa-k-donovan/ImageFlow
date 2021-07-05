#4Plebs API Documentation found here: https://4plebs.tech/foolfuuka/#4plebs-specific-boards-information
# To run make sure to install certificate as explained here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org

import os
import json
import requests
import pandas as pd
import time
from tqdm import tqdm
import PIL
from Website_Settings.file_paths import filepaths

saveDirectory = filepaths.file_server_path + "ImageFlow/img/fourchan/"

def download_image(url):
    print("Started download")
    response = requests.get(url, stream=True)
    print("response works")

    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    print("Filesize received")

    # get the file name
    file_name = (url.split("/")[-1])
    print("FileName:")
    print(file_name)

    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {file_name}", total=file_size, unit="B",
                    unit_scale=True, unit_divisor=1024)

    with open(saveDirectory + file_name, "wb+") as f:
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



def scrape_4chan(start, end, groups, country_code):
    path = "/home/webapp/Digital-Democracies-Instititute-Website/DDI_Website/ImageFlow/data/fourchan"

    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed  - possible directory already exists" % path)
    else:
        print("Successfully created the directory %s" % path)

    image_extensions = ['.jpg', '.png', '.jpeg', '.gif']   # case-insensitive (upper/lower doesn't matter)

    # CHANGE THESE SETTINGS!
    counter = 0
    total_posts = 0
    output_df = []

    current_page = 0

    # incase it was only one item!
    if not type(groups) == list:
        groups = [groups]

    for group in groups:
        #TODO: What filesystem should we use for our database?
        # print("The current working directory is " + saveDirectory)


        # Get the 4chan board catalog JSON file and open it
        base_url = "http://archive.4plebs.org/_/api/chan/search/?boards=" + group + "&start="+ start +"&end=" + end + "&country=" + country_code + "&page=" + str(current_page)
        base_url = str(base_url)
        print(base_url)

        result = requests.get(base_url,
            headers={'User-Agent': 'Mozilla/5.0'})

        print(result)
        result.raise_for_status()

        result = json.loads(result.text)["0"]["posts"]

        pd_result = pd.json_normalize(result)
        df = pd.DataFrame(pd_result)

        while current_page != None:

            base_url = "http://archive.4plebs.org/_/api/chan/search/?boards=" + group + "&start=" + start + "&end=" + end + "&country=" + country_code + "&page=" + str(current_page)
            time.sleep(20)

            result = requests.get(base_url,
                                  headers={'User-Agent': 'Mozilla/5.0'})
            print(result)
            result.raise_for_status()
            result = json.loads(result.text)["0"]["posts"]

            pd_result = pd.json_normalize(result)
            df = pd.DataFrame(pd_result)

            for i in range(0, len(df)):
                total_posts += 1
                try:
                    image_url = df['media.media_link'][i]
                except Exception as ex_media:
                    print("No media.media_link.")
                    continue

                if not isinstance(image_url, str):
                    continue

                # lets make sure we get the media types we care about
                download = False
                for ext in image_extensions:
                    if ext in image_url:
                        download = True
                        break

                if not download:
                    continue

                file_name = download_image(image_url)
                print(dimension)
                counter += 1

                try:
                    username = df['name'][i]
                    timestamp = df['timestamp'][i]
                    country = df['poster_country_name'][i]

                    group_name = df['board.shortname'][i]

                    row = {"file_name": file_name, "imageURL": image_url, "group": group_name, "username": username, "timestamp": timestamp, "country":country, "numComments": 0, "score": 0, "platform": "4Chan", "abs_file_path": saveDirectory + file_name, "dimensions": dimension}
                    output_df.append(row)

                except Exception as ex1:
                    print("Could not retrieve info.")

            current_page += 1

            # if current_page == 10:
            #     current_page = None   

    # Output is Pandas Dataframe
    df = pd.DataFrame(output_df)

    print("Total posts searched: " + str(total_posts))
    print("Script completed")

    return df


# scrape_4chan('08/25/2020', '08/26/2020', "pol", "CA")

