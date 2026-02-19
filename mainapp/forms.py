from django import forms
from mainapp.models import Blog

class Blogform(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title','subtitle','author','content','image']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control mt-2 mb-4'}),
            'subtitle': forms.TextInput(attrs={'class':'form-control mt-2 mb-4'}),
            'author': forms.TextInput(attrs={'class':'form-control mt-2 mb-4'}),
            'content': forms.Textarea(attrs={'class':'form-control mt-2 mb-4','rows':'4'}),
            'image': forms.ClearableFileInput(attrs={'class':'form-control mt-2 mb-4'}),
        }