from django import forms
from .models import ForumPost, Reply

class ForumPostForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = ForumPost
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tiêu đề đề xuất'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nội dung đề xuất', 'rows': 6}),
        }


class ReplyForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nhập bình luận...', 'rows': 3}),
        }


images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

class Meta:
    model = ForumPost
    fields = ['title', 'content']
    widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tiêu đề đề xuất'}),
        'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nội dung đề xuất', 'rows': 6}),
    }


images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

class Meta:
    model = Reply
    fields = ['content']
    widgets = {
        'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nhập bình luận...', 'rows': 3}),
    }
