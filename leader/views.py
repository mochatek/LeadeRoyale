from django.shortcuts import render
from datetime import datetime
import requests
import os

def index(request):
    context = {"members":None}
    if request.method == 'GET':
        if 'tag' in request.GET:
            url = "https://api.royaleapi.com/clan/" + request.GET["tag"]
            headers = {
                'auth': os.environ.get('API_KEY',"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MzEwNCwiaWRlbiI6IjYyODIzMTc1Nzc4MjcxMjM0MCIsIm1kIjp7InVzZXJuYW1lIjoibW9jaGEiLCJkaXNjcmltaW5hdG9yIjoiMjY1NCIsImtleVZlcnNpb24iOjN9LCJ0cyI6MTU2OTg1Mjc0NjMyN30.xzgoRQNT0Iw1fX25918tsKOzFUflSpxKtPJE0B0Thxg")
                }
            response = requests.request("GET", url, headers=headers)
            if response.status_code == 200:
                d = response.json()
                for m in d["members"]:
                    today = datetime.today()
                    seen_date = datetime.strptime(datetime.strptime(m['lastSeen'], "%Y-%m-%dT%H:%M:%SZ").strftime("%d-%b-%Y"),"%d-%b-%Y")
                    days = (today - seen_date).days
                    if days > 0:
                        m["lastSeen"] =  str(days) + " Days ago"
                    else:
                        m["lastSeen"] = "Active"
                context = {
                    "members":d["members"],
                    "req_trophy":d["requiredScore"],
                    "name":d["name"],
                    "score":d["score"],
                    "war_trophy":d["warTrophies"],
                    "member_count":d["memberCount"],
                    "badge":d["badge"]["image"],
                    "donation":d["donations"],
                    "location":d["location"]["code"],
                    "type":d["type"]
                    }
            else:
                context["message"] = True
    return render(request,'leader/index.html',context)
