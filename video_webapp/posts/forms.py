from django import forms
from .models import Post, Comment

class CommentForm(forms.ModelForm):
  comment = forms.CharField(widget=forms.Textarea)

  class Meta:
    model = Comment
    fields = ('comment',)
