from django import forms
from .models import Post, Document


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content', 'author']

    def clean_title(self):
        title = self.cleaned_data['title']

        if len(title) < 5:
            raise forms.ValidationError(
                "Title must contain at least 5 characters."
            )

        return title

    def clean_content(self):
        content = self.cleaned_data['content']

        if len(content) < 10:
            raise forms.ValidationError(
                "Content must contain at least 10 characters."
            )

        return content


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ["title", "file"]