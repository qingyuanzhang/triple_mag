
#coding=utf-8
from django.http import HttpResponse
from django.shortcuts  import render_to_response
from django.template import loader,Context,RequestContext
from django.contrib.auth.decorators import login_required
from engine.models import ExamInfo,Questions,QuestionType

@login_required
def dashboard(request):
    c = RequestContext(request,{})
    return render_to_response("dashboard/dashboard.html",c)
    

