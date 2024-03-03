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
    new_ride.save()
    return redirect("/rides")

def form(request):
  context = {}
  context["form"] = RideForm()
  context["new_ride_form"] = NewRideForm()
  return render(request, "form.html", context)