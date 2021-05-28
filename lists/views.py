from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from lists.models import Item


def home_page(request: HttpRequest):
    if request.method == "POST":
        new_item_text = request.POST["item_text"]
        Item.objects.create(text=new_item_text)
    else:
        new_item_text = ""

    return render(request, "home.html", {"new_item_text": new_item_text})
