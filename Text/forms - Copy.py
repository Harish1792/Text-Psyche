from django import forms


class NameForm(forms.Form):
    for_analysis = forms.CharField(widget=forms.Textarea)
    #text_toB_Analyzed = forms.CharField(widget=forms.Textarea)
    #your_name = forms.CharField(label='Your name', max_length=100)
