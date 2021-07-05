from celery import shared_task
from celery_progress.backend import ProgressRecorder
from .Local_Library.Data_Gathering.fourplebs_image_scraper import scrape_4chan
from .Local_Library.Data_Gathering.reddit_image_scraper import scrape_reddit
from .Local_Library.Data_Gathering.crowdtangle_image_scraper import scrape_facebook
from .Local_Library.Image_Analysis.phash import phash
from .Local_Library.Image_Analysis.pairwise_comparisons import pairwise_comparisons
from .Local_Library.Image_Analysis.clustering import clustering 
from .Local_Library.Data_Visualiztion.df2json import df2json

## TEST ##
from .Local_Library.imf_insert_old import save_data
## TEST ##

from .models import ImageSummary, TaskSummary, PHashSummary, ClusterSummary

import pandas as pd
import PIL

from Website_Settings.file_paths import filepaths

data_dir = filepaths.file_server_path + "ImageFlow/img/"

@shared_task(bind = True , name = "ImageGathering")
def ImageGathering(self, startDate , endDate, platform, subReddit, board, Country, fb_access_tk, access_key, access_secret_key, api_key, api_secret_key, hashtags):
    """
    Returns a dataframe with the downloaded image meta data for storing!

    Here we run based on the platforms chosen
    """

    # runtimeContext = RuntimeContext()
    # runtimeContext.outdir = local_file_system_path

    if platform == []:
        return {"status": "no platform selected"}

    outputs = []
    # check if we have Reddit 
    if "Reddit" in platform:
        # first lets get our sub-reddit list together
        red_df = scrape_reddit(subReddit, startDate, endDate)        
        outputs.append(red_df)

    if "Facebook" in platform:
        # lets process Facebook
        fac_df = scrape_facebook(fb_access_tk, startDate, endDate)
        outputs.append(fac_df)

    if "Twitter" in platform:
        # lets process Twitter
        twit_df = scrape_twitter(access_key, access_secret_key, api_key, api_secret_key, startDate, endDate, hashtags)
        outputs.append(twit_df)
        pass

    if "4Chan" in platform:
        # lets process 4Chan
        chan_df = scrape_4chan(startDate, endDate, board, Country)
        outputs.append(chan_df)

    # now lets merge the results!
    if len(outputs) > 1:
        outputs = pd.concat(outputs, ignore_index=True)
    else:
        outputs = outputs[0]


    ### lets save for tesitng! ### TODO: DELETE THIS
    # outputs.to_csv(local_file_system_path + "output.csv", index=False)
    # outputs = pd.read_csv(local_file_system_path + "output.csv")

    # lets calculate the phash of each image!
    ph = phash(input_p=data_dir)
    outputs = ph.computePhash_df(outputs)
    # outputs.to_csv(local_file_system_path + "output_ph.csv", index=False)

    # lets create a dataframe to store the task summary data before inserting
    task_sum = pd.DataFrame(columns=['image_id', 'task_id'])
    task_sum_i = 1

    # lets push the information to the databse
    num_dups = 0
    num_images = 0

    for row_i, row in outputs.iterrows():
        print("This is the datagathering object:")
        print(ImageGathering)

        # TODO: Causing error here ImageGathering Object has no 'task_id'.
        task_id = ImageGathering.request.id

        #task_id = task_sum.task_id

        # task_id = 2
        num_images = num_images + 1
        # lets first try to get the row we want to see if it exists
        try:
            # check if it exsits
            image = ImageSummary.objects.get(imageURL=row["imageURL"])
            print("Assigning ImageSummary to Image Variable")
            print(image)
            num_dups = num_dups + 1
        except ImageSummary.DoesNotExist:
            print("ImageSummary does NOT EXIST!")
            # if it doesnt then lets make it! 
            image = ImageSummary(task_id = task_id, file_name = row["file_name"], imageURL = row["imageURL"], 
            group = row["group"], username = row["username"], timeStamp = row["timestamp"], country = row["country"], numComments = row["numComments"],
            score = row["score"], platform = row["platform"], PHash = row["PHash"], PHash_gs = row["PHash_gs"] )
            # lets save our new row!
            image.save()

        except Exception as e:
            print("Failed with: " + str(e))

        # now lets insert into our task summary dataframe!
        #TODO: ERROR: local variable 'image' referenced before assignment
        try:
            task_sum.loc[task_sum_i] = [image.id, task_id]
            print("Image.id" + str(image.id))
            task_sum_i = task_sum_i + 1
        except ex as Exception1323:
            print("local variable image error")
        
    # now lets insert into the task_summ table
    for row_i, row in task_sum.iterrows():
        ts = TaskSummary(image_id = row["image_id"], task_id = row["task_id"])
        ts.save()
    
    # lets transfer the images to another server
    # TODO: needs to be done but in the future!

    # lets create a return value to display extra info on data analysis page!
    context = {
        'num_dups': num_dups,
        'num_images': num_images,
    }

    print(context)
    return context


@shared_task(bind = True , name = "ImageAnalysis")
def ImageAnalysis(self, task_list, identical):
    # ## TEST ##
    # print("starting")
    # # get_data()
    # save_data()
    # ## TEST ##

    # lets see if we have ran for these tasks before!
    task_check = len(PHashSummary.objects.filter(task_id = task_list))
    if not task_check == 0:
        # this means we have already ran for this task list!
        print("Image Analysis has already been completed")
        return

    
    # lets retreive all image_id's
    image_ids_obj = TaskSummary.objects.filter(task_id__in = task_list)
    image_ids = []
    
    for i in image_ids_obj:
        image_ids.append(getattr(i, "image_id"))
    
    # once we have the images we can get the phash values and 
    phash_field = "PHash_gs"
    if identical:
        phash_field = "PHash"
    images_obj = ImageSummary.objects.filter(id__in=image_ids)
    images = []
    image_dict = {}
    for i in images_obj:
        image_dict[getattr(i, "id")] = getattr(i, phash_field)
        images.append([getattr(i, "id"), getattr(i, phash_field)])

    # print(images)

    # run the pairwise comp
    pc = pairwise_comparisons(identical)
    pairwise_results = pc.compare(images)
    # print(pairwise_results)

    # save results into the db
    for pair in pairwise_results:
        phash_row = PHashSummary(image1_id = pair[0][0], image2_id = pair[0][1], task_id = task_list
        , ham_dist = pair[1], identical = identical)
        phash_row.save()

    # run clustering
    print("starting Clustering")
    clus = clustering()
    clustering_results = clus.cluster(image_dict, pairwise_results)
    print(clustering_results)
    print("Finished Clustering!")
    print(len(clustering_results))

    # save results into db
    for cluster in clustering_results:
        for image in cluster['images']:
            if cluster["cluster_no"] == -1:
                cluster_row = ClusterSummary(clusterNumber = cluster["cluster_no"], image_id = image, medroid_image_id = -1, task_id = task_list)
            else:
                cluster_row = ClusterSummary(clusterNumber = cluster["cluster_no"], image_id = image, medroid_image_id = cluster["medroid_path"], task_id = task_list)

            cluster_row.save()
    
    return # context


@shared_task(bind = True , name = "ImageVisualization")
def ImageVisualization(self):
    # here we proccess the data! 
    # lets pull the data and join ,, and ,, 

    sql_to_run = '''
    SELECT
    ics.id
    , ics."clusterNumber" as "cluster"
    , iis."imageURL"
    , iis.file_name as "FileName"
    , iis.platform as "SocialMedia"
    , iis.group as "group"
    , iis.country
    , iis.username as "UserName"
    , iis."timeStamp" as "TimeStamp"
    , ics.created_date as "datetime"

    FROM imf_cluster_summary ics
    INNER JOIN imf_image_summary iis ON ics.image_id = iis.id 
    '''

    
    # lets make sure we have a cluster to pulls
    if not ClusterSummary.objects.filter().count() > 0:
        print("No rows to pull from!")
        return False

    latest_Task_row = ClusterSummary.objects.order_by('-created_date')[0].task_id
    if not latest_Task_row == "":
        sql_to_run = sql_to_run + "WHERE ics.task_id = '" + latest_Task_row.replace("'", "*").replace("*", "''") + "'"
    
    cluster_rows = ClusterSummary.objects.raw(sql_to_run)

    reporting_df = pd.DataFrame(columns = ['cluster', 'imageURL','FileName', 'SocialMedia', 'group', 'country', 'UserName', 'TimeStamp', 'datetime', 'Dimensions']) 
    reporting_df_i = 1


    # Now lets set it up into a df!
    for row in cluster_rows:
        # lets build the file_path
        file_path = row.FileName

        # lets get the dimensions of the image!
        img_dim = ""
        sm = row.SocialMedia
        if row.SocialMedia == "4Chan":
            sm = "fourchan"            

        with PIL.Image.open(data_dir + sm + "/" + file_path) as image:
            width, height = image.size
            img_dim = str(width) + " " + str(height)

        # now lets insert into the dataframe!
        reporting_df.loc[reporting_df_i] = [row.cluster, row.imageURL, row.FileName, row.SocialMedia, row.group, row.country, row.UserName, row.TimeStamp, row.datetime, img_dim]
        reporting_df_i = reporting_df_i + 1
    
    # lets give the panadas dataframe to df2json
    # TODO: move this into the image analysis so when visualizing it will be faster!
    df2json(reporting_df)

    # finally lets return so that the html page can load
    return True


@shared_task(bind = True , name = "CodeofConduct")
def CodeofConduct(self):
    return True