from django import forms

class InstagramPostForm(forms.Form):
    caption = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter your caption here...'}),
        max_length=2200,
        required=True,
        label='Caption'
    )
    summary = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': 'readonly'})
        )

    image_url = forms.URLField(
        widget=forms.URLInput(attrs={'placeholder': 'https://example.com/image.jpg'}),
        required=True,
        label='Image URL'
    )
    scheduled_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False,
        label='Scheduled Time'
    )