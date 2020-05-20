import json
import logging
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', filename="systeem.log", level=logging.INFO)

def livesign(request):
    pass
@csrf_exempt
def error(request):
    data = str(request.body)[2:-1]
    json_data = json.loads(data).get("ojson")
    logging.error(f"{error}")
    return JsonResponse({"response": True, "error": None})