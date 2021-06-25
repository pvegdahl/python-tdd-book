from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from lists.forms import ItemForm, ExistingListItemForm
from lists.models import List


def home_page(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html", {"form": ItemForm()})


def view_list(request: HttpRequest, list_id: str) -> HttpResponse:
    the_list = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=the_list)
    if request.method == "POST":
        form = ExistingListItemForm(for_list=the_list, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(the_list)
    return render(request, "list.html", {"list": the_list, "form": form})


def new_list(request: HttpRequest) -> HttpResponse:
    form = ItemForm(data=request.POST)
    if form.is_valid():
        the_new_list = List.objects.create()
        form.save(for_list=the_new_list)
        return redirect(the_new_list)
    else:
        return render(request, "home.html", {"form": form})
