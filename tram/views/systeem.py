import json
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', filename="systeem.log", level=logging.INFO)

def livesign(request):
    pass

def error(request):
    data = str(request.body)[2:-1]
    json_data = json.loads(data).get("ojson")
    logging.error(f"{error}")