from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from PIL import Image

# Create your models here.
class Post(models.Model):
  title = models.CharField(max_length=100)
  content = models.TextField()
  date_posted = models.DateTimeField(default=timezone.now) # passing in function
  author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE) # delete post if user is deleted
  # optional video field
  video = models.FileField(blank=True, null=True, upload_to='videos/%Y/%m/%d/',
                           validators=[FileExtensionValidator(allowed_extensions=['mp4', 'ogb', 'webm'])]) 
  video_thumbnail = models.ImageField(blank=True, default='default_thumbnail.jpg', upload_to='thumbnails/%Y/%m/%d/')

  # For resizing thumnail
  # Possibly use to create thumbnail?
  def save(self, *args, **kwargs): 
    super().save(*args, **kwargs)

    thumbnail = Image.open(self.video_thumbnail.path)
    output_size = (160, 90)
    thumbnail.thumbnail(output_size)
    thumbnail.save(self.video_thumbnail.path)

  def __str__(self):
    return self.title

  # Gets the url from the post using reverse function
  def get_absolute_url(self):
    return reverse('post-detail', kwargs={'pk': self.pk})