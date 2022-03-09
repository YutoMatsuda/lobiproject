from django.shortcuts import render

# Create your views here.

def signupview(request):
    print(request.POST.get('username_data'))
    return render(request,'signup.html', {'somedata':100})

def topview(request):
    print(request.POST.get('username_data'))
    return render(request,'top.html', {'somedata':100})