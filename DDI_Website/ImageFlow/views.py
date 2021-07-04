from django.shortcuts import render,redirect
from .forms import Image_Gathering, Image_Analysis
from .tasks import ImageGathering as tasks_ImageGathering
from .tasks import ImageAnalysis as tasks_ImageAnalysis
from .tasks import ImageVisualization as tasks_ImageVisualization
# from .tasks import CodeOfConduct as tasks_CodeofConduct

from Home.models import UserExtensionModel
from django_celery_results.models import TaskResult
import json
import ast

def ImageGathering(request):
    homeHTML = 'ImageFlow/ImageGathering.html'
    gather_form = Image_Gathering()

    currentUser = request.user
    currentUserModelExt = UserExtensionModel.objects.filter(user = currentUser)

    context = {
        'gather_form': gather_form,
       }
    
    if request.method == 'POST':
        submited_data = request.POST

        startDate = submited_data["startDate"]
        endDate = submited_data["endDate"]
        platform = submited_data.getlist('choice_platform')
        subReddit = submited_data["subReddit"]
        board = submited_data["board"]
        Country = submited_data["Country"]
        fb_access_tk = submited_data["access_token"]
        access_key = submited_data["access_key"]
        access_secret_key = submited_data["access_secret_key"]
        api_key = submited_data["api_key"]
        api_secret_key = submited_data["api_secret_key"]
        hashtags = submited_data["hashtags"]

        ### TESTING
        print("startDate = " + startDate)
        print("endDate = " + endDate)
        print("platform = " + str(platform))
        print("subReddit = " + subReddit)
        print("board = " + board)
        print("Country = " + Country)
        print("fb_access_tk = " + fb_access_tk)
        print("access_key = " + access_key)

        if ',' in subReddit:
            subReddit = subReddit.split(',')
        if isinstance(subReddit, str):
            subReddit = [subReddit]
        
        if ',' in board:
            board = board.split(',')
        if isinstance(board, str):
            board = [board]
        
        #tasks_ImageGathering(startDate, endDate, platform, subReddit, board, Country, fb_access_tk)
        task = tasks_ImageGathering.delay(startDate , endDate, platform, subReddit, board, Country, fb_access_tk, access_key, access_secret_key, api_key, api_secret_key, hashtags)
        # task_id = task.task_id
        numTasks = TaskResult.objects.all().count() + 1
        currentUserModelExt.update(arrayTasksCompleted=currentUserModelExt[0].arrayTasksCompleted + [numTasks])
        return redirect('/ImageFlow/ImageGathering/')

    return render(request, homeHTML , context)  

def ImageAnalysis(request):
    """
    Iterate through User Extension Model, thus getting all the tasks this user has searched for. 
    All done by getting the celery details

    Then during the iteration, match the task with all of its details. In order to get details for "Names"
    """

    currentUser = request.user
    currentUserModelExt = UserExtensionModel.objects.filter(user = currentUser)
    currentUserModelExt_arrayTasksCompleted = currentUserModelExt[0].arrayTasksCompleted

    homeHTML = 'ImageFlow/ImageAnalysis.html'
    analysis_form = Image_Analysis()

    if request.method == 'POST':
        # lest parse submitted data in prep for tasks_ImageAnalysis function
        submited_data = request.POST
        print(submited_data)

        Task_id = submited_data["Task_ids"].split(",")

        try:    
            Identical = submited_data["Identical"]
            Identical = True
        except:
            Identical = False
        
        # now lets pass it to the tasks.py
        tasks_ImageAnalysis(Task_id , Identical)
        # task = tasks_ImageAnalysis.delay(Task_id , Identical)
        # task_id = task.task_id
        # numTasks = TaskResult.objects.all().count() + 1
        # currentUserModelExt.update(arrayTasksCompleted = currentUserModelExt[0].arrayTasksCompleted + [numTasks])

        return redirect('/ImageFlow/ImageAnalysis/')

    tableRow = []
    
    try:
        task_id = TaskResult.objects.filter(id = currentUserModelExt_arrayTasksCompleted[-1])[0].task_id
    except IndexError:
        task_id = None

    for taskNumber in currentUserModelExt_arrayTasksCompleted:
        try:
            task = TaskResult.objects.filter(id = taskNumber)[0]
            if task.task_name == "ImageGathering":
                args = task.task_args
                # lets convert it to a list!
                args = ast.literal_eval("[" + args[1:-1] + "]")
                # print(args)

                result = json.loads(task.result)
                # print(result)

                status = task.status
                # print(status)

                # for plat in args[2]:
                try:
                    tableRow.append([ task.task_id, args[2], args[0], args[1], args[3], args[4], args[5], result["num_dups"], result["num_images"], status ])
                # print([task_id] + args )       
                except:
                    tableRow.append([ task.task_id, args[2], args[0], args[1], args[3], args[4], args[5], 0, 0, status ])

        except IndexError:
            pass
            # return redirect('/Twitter/results/')

    # print(tableRow)
    context = {
        'task_id': task_id,
        'tasksData' : tableRow,
        'form': analysis_form,
       }

    return render(request, homeHTML , context)



def ImageVisualization(request):
    homeHTML = 'ImageFlow/ImageVisualization.html'

    ## run  task to make json! 
    # task = tasks_ImageVisualization.delay()
    task = tasks_ImageVisualization()


    ## task is done lets load page! 
    context = {
        'nothingggg': "",
       }

    return render(request, homeHTML , context) 



def visualization_json(request):
    # make it return the appropriate one by putting it in this url!
    homeHTML = 'ImageFlow/viz_cleaned_data.json'

    # need to move all the images to the right folder to show!

    ## task is done lets load page! 
    context = {
        'nothingggg': "",
       }

    return render(request, homeHTML , context) 


def CodeofConduct(request):
    homeHTML = 'ImageFlow/CodeofConduct.html'

    ## run  task to make json! 
    # task = tasks_ImageVisualization.delay()
    #task = tasks_CodeofConduct()


    ## task is done lets load page! 
    context = {
        'nothingggg': "",
       }

    return render(request, homeHTML , context)  
