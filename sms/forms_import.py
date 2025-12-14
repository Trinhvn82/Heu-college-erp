from django import forms

class RenterImportForm(forms.Form):
    file = forms.FileField(label='Chọn file Excel', required=True)
