from django import forms
from .models import Post, Comment
 
class NewPostForm(forms.ModelForm):
    # removes the default label of content
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols':50,
              'style':'resize:none;','placeholder':'Type new post here' }), label='')
    class Meta:
        model = Post
        fields = ['content']
class NewCommentForm(forms.ModelForm):
	text = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':50,
		'style':'resize:none;','placeholder':'Write a Comment' }), label='')
	class Meta:
		model = Comment
		fields = ['text']