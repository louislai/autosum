from django.http import HttpResponse
from django.shortcuts import render
from analyzer.forms import SummarizerForm

def index(request):
    form  = SummarizerForm(auto_id=False)
    if request.method=='POST':
        form = SummarizerForm(request.POST)
        if form.is_valid():
          cd = form.cleaned_data
          url = cd.get('article_url')
          return HttpResponseRedirect('/')

    return render(request, 'index.html', {'form': form})
# Create your views here.
