from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from lists.models import Item, List


def home_page(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html")


def view_list(request: HttpRequest, list_id: str) -> HttpResponse:
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(request, "list.html", {"items": items})


def new_list(request: HttpRequest) -> HttpResponse:
    the_new_list = List.objects.create()
    Item.objects.create(text=(request.POST["item_text"]), list=the_new_list)
    return redirect(f"/lists/{the_new_list.id}/")


def add_item(request: HttpRequest, list_id: str) -> HttpResponse:
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST["item_text"], list=list_)
    return redirect(f"/lists/{list_.id}/")
