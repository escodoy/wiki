from django.shortcuts import render, redirect
import markdown2

import re
from random import choice
from . import util


def index(request):
    if request.GET.get('q'):
        return search(request, request.GET['q'])
    elif request.GET.get('newtitle'):
        return makepage(request, request.GET['newtitle'], request.GET['content'])
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def navigate(request, title):
    found = util.get_entry(title)
    if found:
        return render(request, "encyclopedia/entry.html", {
            "entry_page": markdown2.markdown(found),
            "entry_title": title
        })
    else:
        return render(request, "encyclopedia/missing.html", {
            "entry_title": title.capitalize()
        })

def search(request, title):
    entries = util.list_entries()

    if title.upper() in map(str.upper, entries):
        return navigate(request, title)
    
    r = re.compile(r'.*' + re.escape(title) + r'.*', re.IGNORECASE)
    matches = list(filter(r.match, entries))
    
    if matches: 
        return render(request, "encyclopedia/results.html", {
            "title": title,
            "results": matches
        })
    else:
        return render(request, "encyclopedia/missing.html", {
            "entry_title": title.capitalize()
        })

def new_page(request):
    return render(request, "encyclopedia/newpage.html")

def makepage(request, title, content):
    entries = util.list_entries()
    
    if title.upper() in map(str.upper, entries):
        return render(request, "encyclopedia/duplicateError.html", {
            "title": title
        })
    else:
        util.save_entry(title, content)
        return redirect("index")

def random(request):
    selected = choice(util.list_entries())
    return navigate(request, selected)