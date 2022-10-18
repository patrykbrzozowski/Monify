from django.shortcuts import render

def index(request):
    return render(request, 'website/index.html')

def app_info(request):
    return render(request, 'website/app_info.html')

def methods_info(request):
    return render(request, 'website/methods_info.html')

# def error_404(request, exception):
#     return render(request, 'not-found.html')
