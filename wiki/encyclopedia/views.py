from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from markdown2 import markdown
from django.urls import reverse
from django import forms
from random import randint

from django.template import loader

from . import util


class NewEntryForm(forms.Form):
    title = forms.CharField(
        label="Title", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    entry = forms.CharField(
        label="Create Entry", widget=forms.Textarea(attrs={"class": "form-control"})
    )


class EditEntryForm(forms.Form):
    title = forms.CharField(
        label="Title", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    entry = forms.CharField(
        label="Edit Entry", widget=forms.Textarea(attrs={"class": "form-control"})
    )


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, entry):
    content = util.get_entry(entry)
    if content is None:
        return render(
            request,
            "encyclopedia/not_found.html",
            {"msg": f"{entry} does not exist in the encyclopedia", "title": entry},
        )

    else:
        return render(
            request,
            "encyclopedia/entry.html",
            {
                "title": entry,
                "content": markdown(content),
            },
        )


def search(request):
    query = request.GET.get("q", "")
    if util.get_entry(query):
        return HttpResponseRedirect(reverse("entry"), args=(query,))

    entries = util.list_entries()
    results = []
    for entry in entries:
        if query.lower() in entry.lower():
            results.append(entry)
    return render(
        request,
        "encyclopedia/results.html",
        {"results": list(sorted(results)), "query": query},
    )


def create(request):
    if request.method == "POST":
        entries = util.list_entries()
        form = NewEntryForm(request.POST)
        if form.is_valid():
            entry = form.cleaned_data["entry"]
            title = form.cleaned_data["title"]
            if title in entries:
                return render(
                    request,
                    "encyclopedia/error.html",
                    {"message": f"The entry '{title}' already exists"},
                )
            else:
                util.save_entry(title, entry)
            return HttpResponseRedirect(reverse("entry", args=(title,)))

    return render(request, "encyclopedia/create.html", {"form": NewEntryForm()})


def edit(request, title):
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["entry"]
            util.save_entry(title, content)
            return render(
                request,
                "encyclopedia/entry.html",
                {
                    "content": markdown(util.get_entry(title)),
                    "title": title,
                },
            )
        else:
            message: "Invalid form submission"
            return render(request, "encyclopedia/edit.html", {"message": message})
    return render(
        request,
        "encyclopedia/edit.html",
        {
            "form": EditEntryForm(
                initial={"entry": util.get_entry(title), "title": title}
            ),
            "title": title,
        },
    )


def random(request):
    # n.B. Could not get 'choice()' to import; worked in terminal though
    list = util.list_entries()
    length = len(list)
    random_num = randint(0, length - 1)
    return render(
        request,
        "encyclopedia/entry.html",
        {
            "content": markdown(util.get_entry(list[random_num])),
            "title": list[random_num],
        },
    )


# Example of HttpResponse object
def my_view(request):
    path = request.path
    method = request.method
    encoding = request.encoding
    user = request.user
    get = request.GET
    headers = request.headers
    return render(
        request,
        "encyclopedia/my_template.html",
        context={
            "path": path,
            "method": method,
            "encoding": encoding,
            "user": user,
            "get": get,
            "headers": headers,
        },
    )
