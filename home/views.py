from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'home/index.html')

def admin_redirect_view(request):
    return redirect('/admin/')

def contact(request):
    return render(request, 'home/contact.html')

def about(request):
    return render(request, 'home/about.html')