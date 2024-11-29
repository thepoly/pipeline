# postline/forms.py

from django import forms

class InstagramPostForm(forms.Form):
    add_all_paragraphs = forms.BooleanField(required=False, label='Add all paragraphs')
    paragraph = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Select Paragraphs'
    )

    def __init__(self, *args, **kwargs):
        paragraphs = kwargs.pop('paragraphs', [])
        super(InstagramPostForm, self).__init__(*args, **kwargs)
        self.fields['paragraph'].choices = paragraphs
        if not paragraphs:
            self.fields['paragraph'].widget = forms.HiddenInput()
