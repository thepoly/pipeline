from django import forms

class InstagramPostForm(forms.Form):
    add_all_paragraphs = forms.BooleanField(required=False, label="Add all paragraphs")
    generate_title_image = forms.BooleanField(required=False, label="Generate Title Image")
    paragraph = forms.MultipleChoiceField(
        choices=[],  # Choices will be set dynamically
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    extra_text = forms.CharField(required=False, max_length=50, label="Extra text (e.g., 'NEWS')")
    extra_text_position = forms.ChoiceField(
        choices=[("left", "Left"), ("right", "Right")],
        required=False,
        label="Extra text position"
    )

    def __init__(self, *args, **kwargs):
        paragraphs = kwargs.pop('paragraphs', [])  # Extract paragraphs from kwargs
        super().__init__(*args, **kwargs)
        self.fields['paragraph'].choices = paragraphs  # Set the paragraph choices dynamically


            