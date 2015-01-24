from django import forms

class SummarizerForm(forms.Form):
  article_url = forms.URLFields(max_length=255)
  