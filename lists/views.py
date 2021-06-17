from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from lists.models import Item, List


def home_page(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html")


def view_list(request: HttpRequest, list_id: str) -> HttpResponse:
    list_ = List.objects.get(id=list_id)
    if request.method == "POST":
        Item.objects.create(text=request.POST["item_text"], list=list_)
        return redirect(f"/lists/{list_.id}/")
    return render(request, "list.html", {"list": list_})


def new_list(request: HttpRequest) -> HttpResponse:
    the_new_list = List.objects.create()
    item = Item(text=(request.POST["item_text"]), list=the_new_list)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        the_new_list.delete()
        return render(request, "home.html", {"error": "You can't have an empty list item"})
    return redirect(f"/lists/{the_new_list.id}/")
