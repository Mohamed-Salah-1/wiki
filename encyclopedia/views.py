from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown
from . import util
import random


def index(request):
    entries = util.list_entries()
    css_file = util.get_entry('CSS')
    coffee = util.get_entry('coffee')
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# converting md to html
def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if not content:
        return None
    else:
        return markdowner.convert(content)


def entry(request, title):
    if title in util.list_entries():
        html_content = convert_md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title, "content": html_content
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })

def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = convert_md_to_html(entry_search)

        if html_content:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search, "content": html_content
            })
        else:
            recommendation = []
            all_entries = util.list_entries()

            for entry in all_entries:
                if entry_search.lower() in entry.lower():
                    recommendation.append(entry)
                
            if recommendation:
                return render(request, "encyclopedia/search.html", {
                    "recommendation": recommendation
                })
            else:
                return render(request, "encyclopedia/error.html", {
                    "message":"Entry not Found."
                })

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "Entry page already exists"
            })
        else:
            util.save_entry(title, content) # from util.py, use functiom save.entry
            html_content = convert_md_to_html(title)
            return render(request, "encyclopedia/new.html", {
                "title": title, "content": html_content
            })

def edit(request):
    if request.method == 'POST':
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html" , {
            "title":title, "content":content
        })
def save_edit(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        html_content = convert_md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title, "content": html_content
        })

def rand(request):
    all_entries = util.list_entries()
    rand_entry = random.choice(all_entries)
    html_content = convert_md_to_html(rand_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": rand_entry, "content": html_content
        })

