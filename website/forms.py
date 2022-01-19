from django import forms


class ContactForm(forms.Form):
    """ Contact form for users to submit """
    name = forms.CharField(label='Your name', max_length=50)
    email = forms.EmailField(max_length=50)
    message = forms.CharField(widget=forms.Textarea)
