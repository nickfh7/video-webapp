from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.validators import FileExtensionValidator

# The Post class is a model for creating genereic posts
# These posts must include a title and content, but
# not a video or video thumbnail
class Post(models.Model):
  title = models.CharField(max_length=100)
  content = models.TextField()
  date_posted = models.DateTimeField(default=timezone.now) # passing in function for timezone
  author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE) # CASCADE will delete post if user is deleted

  # Optional video fields
  # blank means that it is not required on the form when posting
  # null allows the database to not have an entry (i.e. no default)
  video = models.FileField(blank=True, null=True, upload_to='videos/%Y/%m/%d/',
                           validators=[FileExtensionValidator(allowed_extensions=['mp4', 'ogb', 'webm'])]) 
  video_thumbnail = models.ImageField(blank=True, default='default_thumbnail.jpg', upload_to='thumbnails/%Y/%m/%d/')

  # For resizing thumnail
  # Possibly use to create thumbnail?
  def save(self, *args, **kwargs):
    # Use the original save first 
    super().save(*args, **kwargs)

    # Resize the thumbnail
    thumbnail = Image.open(self.video_thumbnail.path)
    output_size = (160, 90)
    thumbnail.thumbnail(output_size)
    thumbnail.save(self.video_thumbnail.path)

  def __str__(self):
    # Use title as the string for this post
    return self.title

  # Gets the url from the post using reverse function
  def get_absolute_url(self):
    return reverse('post-detail', kwargs={'pk': self.pk})

# Create comment class, use ForiegnKey with Post
