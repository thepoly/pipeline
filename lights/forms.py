from django import forms


class ColorForm(forms.Form):
    R = forms.IntegerField(max_value=255, min_value=0)
    G = forms.IntegerField(max_value=255, min_value=0)
    B = forms.IntegerField(max_value=255, min_value=0)
