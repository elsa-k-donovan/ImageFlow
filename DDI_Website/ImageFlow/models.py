from django.db import models
from django.utils import timezone

# Create your models here.
class ImageSummary(models.Model):
    task_id = models.CharField(max_length=50)
    file_name = models.TextField()
    imageURL = models.TextField()
    group = models.TextField()
    username = models.TextField()
    timeStamp = models.PositiveIntegerField()
    country = models.TextField()
    numComments = models.PositiveIntegerField()
    score = models.PositiveIntegerField()
    platform = models.TextField() 
    PHash = models.CharField(max_length = 200)
    PHash_gs = models.CharField(max_length = 200)
    created_date = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        db_table = 'imf_image_summary'
 
class TaskSummary(models.Model):
    image_id = models.IntegerField()
    task_id = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        db_table = 'imf_task_summary'

class PHashSummary(models.Model):
    image1_id = models.IntegerField() # TODO: look for a different model attribute, since these are looking at two different images from Image Summary
    image2_id = models.IntegerField()
    task_id = models.CharField(max_length=400)
    ham_dist = models.PositiveIntegerField()
    identical = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        db_table = 'imf_phash_summary'

class ClusterSummary(models.Model):
    clusterNumber = models.IntegerField()
    image_id = models.IntegerField()
    medroid_image_id = models.IntegerField()
    task_id = models.CharField(max_length=400, default="")
    created_date = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        db_table = 'imf_cluster_summary'






