# views.py
from django import forms
from django.shortcuts import render, redirect
from .models import Url
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
import random
import string
from django.http import Http404
from urllib.parse import urljoin

class UrlForm(forms.Form):
    URL = forms.URLField()
    alias = forms.CharField(required=False)

def getAlias():
    return "".join([random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(8)])

def dashboard(request):
    if request.method == "POST":
        form = UrlForm(request.POST)
        if form.is_valid():
            URL = form.cleaned_data['URL']
            alias = form.cleaned_data['alias']
            if not alias:
                alias = getAlias()
            try:
                 # Add "https://" to the URL before saving it
                if not URL.startswith("http://") and not URL.startswith("https://"):
                    URL = "https://" + URL
                Url.objects.create(user=request.user, targetUrl=URL, alias=alias)
                return redirect("dashboard")
            except:
                messages.error(request, "Alias already in use.")
        else:
            messages.error(request, "Invalid URL or alias.")
    else:
        form = UrlForm()
    
    site = get_current_site(request)
    return render(request, "dashboard.html", {"form": form, "domain": site})
    # if request.method == "POST":
    #     URL = request.POST.get("URL")
    #     site = get_current_site(request)
    #     alias = request.POST.get("alias")
    #     if not alias:
    #         alias = getAlias()
    #     try:
    #         Url.objects.create(user=request.user, targetUrl=URL, alias=alias)
    #         return redirect("dashboard")
    #     except:
    #         messages.error(request, "Alias already in use.")
    #         return render(request, "dashboard.html", {"URL": URL, "alias": alias})
    
    # site = get_current_site(request)
    # return render(request, "dashboard.html", {"domain": site})
    
from urllib.parse import urljoin

# ...

def save_url(request, target_url, alias):
    # Add "https://" to the URL if it's missing
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        target_url = "https://" + target_url

    # Save the URL with the correct format
    Url.objects.create(user=request.user, targetUrl=target_url, alias=alias)


def redirect_to_target_page(request, alias):
    try:
        obj = Url.objects.get(alias=alias)
        URL = obj.targetUrl
        full_url = urljoin("https://", URL)  # Add the scheme if it's missing
        return redirect(full_url)
    except Url.DoesNotExist:
        raise Http404("URL not found")
