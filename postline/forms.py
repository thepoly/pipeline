from django import forms

class InstagramPostForm(forms.Form):
    title = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    summary = forms.CharField(widget=forms.Textarea(attrs={'readonly': 'readonly'}))
    instagram_link = forms.URLField(required=False, help_text="Link to the Instagram post")