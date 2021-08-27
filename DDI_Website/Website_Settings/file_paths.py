import os
settings_dir = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))

class filepaths():
    #print("THIS IS THE PROJECT ROOT PATH: " + PROJECT_ROOT)

    file_server_path = os.path.join(PROJECT_ROOT, 'Templates_HTML/static/')
    templates_path = os.path.join(PROJECT_ROOT, 'Templates_HTML/templates/ImageFlow/')

    # file_server_path = '/Volumes/TimeMachine/Meme-Dataset/ImageFlow_deepcopy_no_git/DDI_Website/Templates_HTML/static/'
    # templates_path = '/Volumes/TimeMachine/Meme-Dataset/ImageFlow_deepcopy_no_git/DDI_Website/Templates_HTML/templates/ImageFlow/'
    