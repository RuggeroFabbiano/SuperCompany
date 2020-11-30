"""
Forms for the blog app.:
 - sign-up
 - new/edit post
 - new comment
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from mediumeditor.widgets import MediumEditorTextarea
from .models import Post, Comment

User = get_user_model()

class SignUpForm(UserCreationForm):
    """
    Defines sign-up form as a modified version of the standard UserCreationForm
    """
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=100, required=False,
        help_text="Optional")
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name',
            'last_name', 'email')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "User name"
        self.fields['username'].help_text = mark_safe(""
            "<ul>"
            "<li>At most 150 characters</li>"
            "<li>Only letters, digits and the following characters: @ _ . + -</li>"
            "</ul>")
        # self.fields['username'].widget.attrs.update({'placeholder': 'user name'})
        self.fields['password1'].help_text = mark_safe(""
            "<ul>"
            "<li>At least 8 characters</li>"
            "<li>Cannot be a commonly-used password</li>"
            "<li>Cannot be too similar to other personal information</li>"
            "<li>Cannot be entirely numeric</li>"
            "</ul>")
        self.fields['password2'].help_text = ""
        self.fields['first_name'].label = "Name"
        self.fields['last_name'].label = "Surname"
        self.fields['email'].label = "E-mail address"

class PostForm(forms.ModelForm):
    """
    Defines post form
    """
    class Meta:
        model = Post
        fields = ('title', 'content', 'posted')
        widgets = {'title': MediumEditorTextarea(),
                   'content': MediumEditorTextarea()}
        labels = {'posted': "Post now"}

class CommentForm(forms.ModelForm):
    """
    Defines comment form
    """
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {'content': MediumEditorTextarea()}
        labels = {'content': "Add comment"}
