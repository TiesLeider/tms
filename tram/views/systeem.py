import json
import logging
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
import os
from tms_webapp.settings import BASE_DIR, SYSTEM_LOGFILE_NAME

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', filename=SYSTEM_LOGFILE_NAME, level=logging.INFO)

def livesign(request):
    pass


@csrf_exempt
def error(request):
    data = str(request.body)[2:-1]
    json_data = json.loads(data).get("ojson")
    logging.error(f"{json_data}")
    return JsonResponse({"response": True, "error": None})


@login_required
def change_password(request):
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user) 
                messages.success(request, 'Your password was successfully updated!')
                return redirect('index')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'tram/change_password.html', {
            'form': form
        })

def show_api_log(request):
    response = ""
    with open(os.path.join(BASE_DIR, f'logfiles/api-log-week-{datetime.datetime.now().strftime("%V")}.log'), "r") as logfile:
        for line in logfile.readlines():
            response += line
    return HttpResponse(response, content_type='text/plain')

@login_required
def delete_log(request):
    with open(os.path.join(BASE_DIR, f'logfiles/api-log-week-{datetime.datetime.now().strftime("%V")}.log'), "w") as logfile:
        logfile.write("")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))




