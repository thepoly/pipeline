# postline/forms.py
from django import forms

class InstagramPostForm(forms.Form):
    caption = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter your caption here...'}),
        max_length=2200,
        required=True,
        label='Caption'
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
    add_all_paragraphs = forms.BooleanField(
        required=False,
        label='Add All Paragraphs',
        help_text='Select this to append all paragraphs from the article to the caption.'
    )
    paragraph = forms.MultipleChoiceField(
        choices=[],
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Select Paragraphs to Display',
        help_text='Choose one or more paragraphs from the article to include in your post.'
    )

    def __init__(self, *args, **kwargs):
        paragraphs = kwargs.pop('paragraphs', [])
        super(InstagramPostForm, self).__init__(*args, **kwargs)
        self.fields['paragraph'].choices = paragraphs