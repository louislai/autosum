from django.http import HttpResponseRedirect
from django.shortcuts import render

def index(request):
    if request.method=='POST':
        form = request.POST
        url = form.get('article_url')
        return HttpResponseRedirect('/index')

    return render(request, 'index.html')

def compare(request):
  return render(request, 'compare.html')

def cluster(request):
  return render(request, 'cluster.html')
