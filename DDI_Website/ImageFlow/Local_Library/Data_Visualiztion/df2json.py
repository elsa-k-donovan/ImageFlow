import json
import pandas as pd
import os
from Website_Settings.file_paths import filepaths

# 
data_dir = filepaths.file_server_path + "ImageFlow/reporting/"


# Change these file paths to your specific files.
def df2json(df):
    # CsvFile = 'Meme_Database_dim_size.csv'
    # df = pd.read_csv(CsvFile)

    j = 0
    output = []

    for j in range(len(df['cluster'])):

        cluster = str(df['cluster'].iloc[j])

        imageURL = str(df['imageURL'].iloc[j])
        filename = str(df['FileName'].iloc[j])
        socialmedia = str(df['SocialMedia'].iloc[j])
        group = str(df['group'].iloc[j])
        country = str(df['country'].iloc[j])
        username = str(df['UserName'].iloc[j])
        timestamp = str(df['TimeStamp'].iloc[j])
        datetime = str(df['datetime'].iloc[j])
        # color = str(df['Color'].iloc[j])
        # size = str(df['Size'].iloc[j])
        dimensions = str(df['Dimensions'].iloc[j])

        json_row = {"cluster": cluster}

        y = {"cluster": cluster, "image_url": imageURL, "filename": filename, "socialmedia": socialmedia, "group": group, "country": country,
            "username": username, "timestamp": timestamp, "datetime": datetime, "dimensions": dimensions}

        json_row.update(y)

        output.append(json_row)

    with open('temp.json', 'w') as f:
        json.dump(output, f)

    jsonfile = 'temp.json'

    output = pd.read_json(jsonfile)

    df2 = output.groupby(['cluster']).agg(lambda x: x.tolist())

    df2.to_json(data_dir + 'viz_cleaned_data.json')