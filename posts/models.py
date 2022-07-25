from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class SoftDeleteManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class DeletedRecordManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=True)
    
    
class SoftDeletionModel(models.Model):
    is_deleted = models.BooleanField(null=False, default=False)
    
    objects = SoftDeleteManager()
    deleted_objects = DeletedRecordManager()
    
    class Meta:
        abstract = True
        
    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save(update_fields=["is_deleted"])

    def restore(self):
        self.is_deleted = False
        self.save(update_fields=["is_deleted"])
        
        
class Hashtag(models.Model):
    tag = models.CharField(max_length=255, null=False, unique=True)
    
    def __str__(self):
        return self.tag
     

class Post(SoftDeletionModel):
    title = models.CharField(max_length=255, null=False)
    content = models.CharField(max_length=255, null=False)
    user =  models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    hashtag = models.ManyToManyField(Hashtag, through='PostHashtag', related_name='hashtag_list')
    view_count = models.IntegerField(null=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)