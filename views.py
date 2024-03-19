from .forms import RideForm, NewRideForm


from django.shortcuts import render, redirect

from .models import Person

# relative import of forms
# from .forms import RideForm

# Create your views here.


def index(request):

  context = {}
  context["form"] = RideForm()


  if "stateSearch" in request.GET:
    context["inputExists"] = True
    stateSearch = request.GET["stateSearch"]
    citySearch = ""

    if "citySearch" in request.GET:
      citySearch = request.GET["citySearch"]
    
    context["people"] = Person.objects.filter(destination_city__icontains=citySearch, destination_state__icontains=stateSearch) | Person.objects.filter(origination__icontains=citySearch, destination_state__icontains=stateSearch)

  return render(request, "index_view.html", context)

def about(request):
    return render(request, "about.html")

def create(request):
  if request.method == "POST":
    new_ride = NewRideForm(request.POST)
    if new_ride.is_valid():
        new_ride.save()
        return redirect("/rides")
    else:
        print(new_ride.errors)

    return redirect("/rides")

def form(request):
  context = {}
  context["form"] = RideForm()
  context["new_ride_form"] = NewRideForm()
  return render(request, "form.html", context)

import os
from transformers import pipeline
from .models import Person

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from django.forms.models import model_to_dict
from django.core.serializers import serialize
import json

def ai_interaction(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')

        rides_data = Person.objects.all().order_by('-id')[:5] # only getting last 5 currently

        rides_data_list = [model_to_dict(instance) for instance in rides_data]
        system_message = f"You are trying to help folks get rides based on the data you have in your database: {str(rides_data_list)}. If the following user prompt is not about to asking for ride info, return 'Invalid query. Try again.'"

        chat = ChatOpenAI(model_name="gpt-4", temperature=0)
        messages = [
            SystemMessage(
                content=system_message
            ),
            HumanMessage(
                content=user_input
            ),
        ]

        final_ai_text = chat.invoke(messages)

        parts = str(final_ai_text).split(" response_metadata=")
        content_part = parts[0]
        content = content_part.replace("content='", "")[:-1]
        content = content.replace("\\n", " | ")

        return render(request, 'index_view.html', {'ai_text': content})
    
    return render(request, 'index_view.html')