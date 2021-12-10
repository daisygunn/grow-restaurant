from django import forms
# from crispy_forms.helper import FormHelper

class ContactForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=50)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_class = 'form-horizontal'
    #     self.helper.label_class = 'col-lg-2'  
    #     self.helper.field_class = 'col-lg-8'  