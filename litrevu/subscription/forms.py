from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Recherche utilisateur')