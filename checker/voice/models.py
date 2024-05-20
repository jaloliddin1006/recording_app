from django.db import models

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Audio(BaseModel):
    sentence_id = models.CharField(max_length=255)
    sentence = models.TextField()
    file_path = models.FileField(upload_to='records/')
    status = models.CharField(max_length=10, default='unread')

    def __str__(self):
        return self.sentence