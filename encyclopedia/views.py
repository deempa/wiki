import re
from django.http.response import HttpResponse
from django.shortcuts import render
from django import forms
from django.forms.forms import Form
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
import markdown2

import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entryname):
    if util.get_entry(entryname) == None:
        return render(request, "encyclopedia/entry.html", {
        "entrytitle": "Not Found",
        "entrycontent": "The requested page was not found.",
        })

    return render(request, "encyclopedia/entry.html", {
        "entrytitle": entryname.capitalize(),
        "entrycontent": markdown2.markdown(util.get_entry(entryname))
    })

def search(request):
    if request.method == "POST":
        query_entry_name = request.POST.get("q")
        if util.get_entry(query_entry_name) == None:
            matching = [s for s in util.list_entries() if query_entry_name.capitalize() in s]
            if len(matching) > 0:
                return render(request, "encyclopedia/index.html", {
                "entries": matching
                })
            return redirect('/')  
        else:
            return redirect('/wiki/' + query_entry_name)  


def newpage(request):
    if request.method == "POST":
        entry_title = request.POST.get("entrytitle")
        entry_content = request.POST.get("entrycontent")
        if entry_title in util.list_entries():
            return HttpResponse("This Page Already Exists!")
        else:
            util.save_entry(entry_title, entry_content)
            return redirect('/wiki/' + entry_title)

    return render(request, "encyclopedia/newpage.html")

def editpage(request, entryname):
    if request.method == "POST":
        entry_new_content = request.POST.get('entrycontent')
        util.save_entry(entryname, entry_new_content)
        return redirect(f'/wiki/{entryname}')
    entryconent = util.get_entry(entryname)
    return render(request, "encyclopedia/editpage.html", {
        'entrytitle': entryname,
        'entrycontent': entryconent
    })

def randompage(request):
    random_number = random.randint(1, len(util.list_entries()) - 1)
    random_entry_title = util.list_entries()[random_number]
    return redirect(f'/wiki/{random_entry_title}')