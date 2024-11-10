from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from .models import *


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        pass
