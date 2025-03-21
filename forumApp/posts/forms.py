from dataclasses import fields

from django import forms
from django.core.exceptions import ValidationError
from django.forms import formset_factory

from forumApp.posts.mixins import DisableFieldMixin
from forumApp.posts.models import Post, Comment


class PostBaseForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['approved', 'author']

        error_messages = {
            'title': {
                'required': 'Please enter a title',
            }
        }

class PostCreateForm(PostBaseForm):
    pass


class PostEditForm(PostBaseForm):
    pass


class PostDeleteForm(PostBaseForm, DisableFieldMixin):
    disabled_fields = ('__all__', )


class SearchForm(forms.Form):
    query = forms.CharField(
        label='',
        required=True,
        error_messages={
            'required': 'Please write something'
        },
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search for a post...',
            }
        )
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'content']

        labels = {
            'author': '',
            'content': '',
        }

        error_messages = {
            'author': {
                'required': 'Please enter your name',
            },
            'content': {
                'required': 'Please enter a comment',
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['author'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Your name',
        })

        self.fields['content'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Your comment',
        })

CommentFormSet = formset_factory(CommentForm, extra=1)