from django import forms
from .models import Post
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.urls import reverse


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('Submit', 'submit'))

    text = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'rows': 1,
                'placeholder': 'share something',
            }
        )
    )

    class Meta:
        model = Post
        fields = ['text']
