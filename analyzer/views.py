from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
  return render(request, 'index.html')

def compare(request):
  if request.method=='POST':
    form = request.POST
    url_1 = form.get('article_url_1')
    url_2 = form.get('article_url_2')
    return HttpResponse(url_1 + url_2)
  return render(request, 'compare.html')

def cluster(request):
  if request.method=='POST':
    form = request.POST
    urls = form.get('article_urls')
    return HttpResponse(urls)
  return render(request, 'cluster.html')

def summarize(request):
  if request.method=='POST':
    form = request.POST
    url = form.get('article_url')
    return HttpResponse(url)
