from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from lists.forms import ItemForm
from lists.models import Item, List


def home_page(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html", {"form": ItemForm()})


def view_list(request: HttpRequest, list_id: str) -> HttpResponse:
    the_list = List.objects.get(id=list_id)
    error = None

    if request.method == "POST":
        item = Item(text=(request.POST["item_text"]), list=the_list)
        try:
            item.full_clean()
            item.save()
            return redirect(the_list)
        except ValidationError:
            error = "You can't have an empty list item"
    return render(request, "list.html", {"list": the_list, "error": error})


def new_list(request: HttpRequest) -> HttpResponse:
    the_new_list = List.objects.create()
    item = Item(text=(request.POST["item_text"]), list=the_new_list)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        the_new_list.delete()
        return render(
            request, "home.html", {"error": "You can't have an empty list item"}
        )
    return redirect(the_new_list)
