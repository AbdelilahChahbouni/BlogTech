from django import forms
from .models import Comment , Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body' , 'email']



class ContactForm(forms.Form):
    name = forms.CharField(max_length=150)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)




class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields =['title' , 'body' , 'bg_image' , 'post_image' , 'status']


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields =['title' , 'body' , 'bg_image' , 'post_image' , 'status']
        widgets = {
            "status": forms.Select(choices=Post.Status.choices),
        }

