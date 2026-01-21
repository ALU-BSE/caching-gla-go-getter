from django.http import HttpResponse

def home(_request):
    return HttpResponse("Welcome to SafeBoda. Go to /admin/ or /api/users/")