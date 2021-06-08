from django import forms


class PostForm(forms.Form):
    """
        Форма для создания поста в /app_posts/full_size/create_post.html
    """
    photos = forms.FileField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control',
        'accept': 'image/*',
        'id': 'formFileMultiple',
        'multiple': True,
    }))
    text = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'id': 'floatingTextarea',
        'style': 'height: 300px',
        'placeholder': 'label',
    }), max_length=10000)


class CsvForm(forms.Form):
    """
        Форма CSV файла с постами в /app_posts/full_size/create_post.html
    """
    csv_file = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'form-control mb-3',
        'id': 'formFile',
        'accept': '.csv',
    }))
