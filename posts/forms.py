from django import forms
from .models import posts

class postsform(forms.ModelForm):
    class Meta:
        model = posts
        fields = [
            "title",
            "body",
            # "user"
        ]