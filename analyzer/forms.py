from django import forms

class SummarizerForm(forms.Form):
  article_url = forms.URLField(max_length=255)
  