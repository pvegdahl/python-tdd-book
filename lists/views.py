from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from accounts.models import User
from lists.forms import ItemForm, NewListForm, ExistingListItemForm
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
        the_new_list = List()
        the_new_list.owner = request.user
        the_new_list.save()
        form.save(for_list=the_new_list)
        return redirect(the_new_list)
    else:
        return render(request, "home.html", {"form": form})


def new_list2(request: HttpRequest) -> HttpResponse:
    form = NewListForm(data=request.POST)
    if form.is_valid():
        return redirect(form.save(owner=request.user))
    else:
        return render(request, "home.html", {"form": form})


def my_lists(request: HttpRequest, email: str) -> HttpResponse:
    return render(request, "my_lists.html", {"owner": (User.objects.get(email=email))})
