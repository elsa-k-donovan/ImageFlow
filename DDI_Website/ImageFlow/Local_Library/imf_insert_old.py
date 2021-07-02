import pandas as pd
from os import walk

# # # this will let me go to the scraper for information
# import sys
# sys.path.append('../')

# from Image_Analysis.phash import phash
from ..models import ImageSummary, TaskSummary
import os

source = "/Users/hedayattabesh/Documents/Data/raw data/final_dataset/"
meta_data_filename = "all_metadata_web_app.csv"
img_location = "/Users/hedayattabesh/Documents/scripts/Digital-Democracies-Instititute-Website/DDI_Website/ImageFlow/data/final_dataset/"
image_extensions = ['.jpg', '.png', '.jpeg', '.gif']   # case-insensitive (upper/lower doesn't matter)

### SET VARIABLES FOR NEW META!
task_id = "CanadaElection2019"


def get_data():
    # lets get the the old meta data
    meta_data = pd.read_csv(source + meta_data_filename)
    print(meta_data)

    # lets create a new dataframe for our new meta data!
    new_meta_data = pd.DataFrame(columns = ['task_id', 'file_name','imageURL', 'group', 'username', 'timeStamp', 'country', 'numComments', 'score', 'platform']) 
    new_meta_data_i = 1

    # lets get all files in the Final Dataset! 
    fb_imgs = []
    fc_imgs = []
    red_imgs = []
    twt_imgs = []

    for dp, dn, filenames in os.walk(img_location + 'facebook/'):
        for f in filenames: 
            if os.path.splitext(f)[1].lower() in image_extensions:
                fb_imgs.append([f, os.path.join(dp, f)])
    print("facebook = " + str(len(fb_imgs)))

    for dp, dn, filenames in os.walk(img_location + '4chan/'):
        for f in filenames: 
            if os.path.splitext(f)[1].lower() in image_extensions:
                fc_imgs.append([f, os.path.join(dp, f)])
    print("4chan = " + str(len(fc_imgs)))
    
    for dp, dn, filenames in os.walk(img_location + 'reddit/'):
        for f in filenames: 
            if os.path.splitext(f)[1].lower() in image_extensions:
                red_imgs.append([f, os.path.join(dp, f)])
    print("reddit = " + str(len(red_imgs)))
    
    for dp, dn, filenames in os.walk(img_location + 'twitter/'):
        for f in filenames: 
            if os.path.splitext(f)[1].lower() in image_extensions:
                twt_imgs.append([f, os.path.join(dp, f)])
    print("twitter = " + str(len(twt_imgs)))
    

    for row_i, row in meta_data.iterrows():
        # if row["SocialMedia"] == 'facebook':
        #     for i in fb_imgs:
        #         if i[0] == row["FileName"]:
        #             new_meta_data.loc[new_meta_data_i] = [task_id, i[1], row['imageURL'], row['group'], row['UserName'], row['TimeStamp'], row['country'], 0, 0, row['SocialMedia']]
        #             new_meta_data_i = new_meta_data_i + 1
        
        # if row["SocialMedia"] == '4chan':
        #     for i in fc_imgs:
        #         if i[0] == row["FileName"]:
        #             new_meta_data.loc[new_meta_data_i] = [task_id, i[1], row['imageURL'], row['group'], row['UserName'], row['TimeStamp'], row['country'], 0, 0, row['SocialMedia']]
        #             new_meta_data_i = new_meta_data_i + 1

        # elif row["SocialMedia"] == 'reddit':
        #     for i in red_imgs:
        #         if i[0] == row["FileName"]:
        #             new_meta_data.loc[new_meta_data_i] = [task_id, i[1], row['imageURL'], row['group'], row['UserName'], row['TimeStamp'], row['country'], 0, 0, row['SocialMedia']]
        #             new_meta_data_i = new_meta_data_i + 1
        
        if row["SocialMedia"] == 'twitter':
            for i in twt_imgs:
                if i[0] == row["FileName"]:
                    new_meta_data.loc[new_meta_data_i] = [task_id, i[1], row['imageURL'], row['group'], row['UserName'], row['TimeStamp'], row['country'], 0, 0, row['SocialMedia']]
                    new_meta_data_i = new_meta_data_i + 1
        
    print(new_meta_data)
    new_meta_data.to_csv(img_location + "tmp.csv", index=False)

    print("starting phash calculation")
    ph = phash(input_p=img_location)
    outputs = ph.computePhash_df(new_meta_data)

    new_meta_data.to_csv(img_location + "twt_ph.csv", index=False)

def save_data():
    new_meta_data = pd.read_csv(img_location + "red_fb_ph.csv")
    print(new_meta_data)
    task_sum = pd.DataFrame(columns = ['image_id', 'task_id']) 
    task_sum_i = 1

    for row_i, row in new_meta_data.iterrows():
        if pd.isnull(row["timeStamp"]):
            row["timeStamp"] = 0
        if pd.isnull(row["imageURL"]):
            row["imageURL"] = ""
        if pd.isnull(row["country"]):
            row["country"] = ""

        image = ImageSummary(task_id = row["task_id"], file_name = row["file_name"], imageURL = row["imageURL"], 
        group = row["group"], username = row["username"], timeStamp = row["timeStamp"], country = row["country"], numComments = row["numComments"], 
        score = row["score"], platform = row["platform"], PHash = row["PHash"], PHash_gs = row["PHash_gs"] )
        image.save()

        # now lets insert into our task summary dataframe!
        task_sum.loc[task_sum_i] = [image.id, task_id]
        task_sum_i = task_sum_i + 1

    # now lets insert into the task_summ table
    for row_i, row in task_sum.iterrows():
        ts = TaskSummary(image_id = row["image_id"], task_id = row["task_id"])
        ts.save()



# save_data()

