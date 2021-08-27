from django.urls import path
from . import views as image_views


urlpatterns = [
    path('ImageGathering/', image_views.ImageGathering, name = 'image-gathering'),
    path('ImageAnalysis/' , image_views.ImageAnalysis , name = 'image-analysis'),
    path('ImageVisualization/' , image_views.ImageVisualization , name = 'image-visualization'),
    path('viz_cleaned_data.json' , image_views.visualization_json , name = 'visualization_json')
    #path('similar_imageset_dimensions.json' , image_views.visualization_json , name = 'visualization_json')
    #path('img/' , image_views.img_visuals , name = 'img_visuals')
    #path('CodeOfConduct/' , image_views.CodeOfConduct , name = 'code-of-conduct')
]