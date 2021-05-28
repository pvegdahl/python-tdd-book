from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from lists.models import Item


def home_page(request: HttpRequest):
    item = Item()
    item.text = request.POST.get("item_text", "")
    item.save()

    return render(request, "home.html", {"new_item_text": item.text})
