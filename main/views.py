from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache

from .forms import ContactMessageForm, GalleryPasswordForm
from .models import FriendProfile, GalleryCategory


def home(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you — your note has been received.")
            return redirect("home")
        messages.error(request, "Please check the contact form and try again.")
    else:
        form = ContactMessageForm()

    categories = GalleryCategory.objects.prefetch_related("images")
    return render(request, "main/home.html", {
        "categories": categories,
        "contact_form": form,
    })


@never_cache
def category_detail(request, slug):
    category = get_object_or_404(GalleryCategory, slug=slug)
    session_key = f"gallery_unlocked_{category.pk}"

    if request.session.get(session_key):
        return render(request, "main/gallery_detail.html", {
            "category": category,
            "images": category.images.all(),
        })

    if request.method == "POST":
        form = GalleryPasswordForm(request.POST)
        if form.is_valid() and category.check_password(form.cleaned_data["password"]):
            request.session[session_key] = True
            return redirect("category_detail", slug=category.slug)
        form.add_error("password", "That password is not correct.")
    else:
        form = GalleryPasswordForm()

    return render(request, "main/password_prompt.html", {
        "category": category,
        "form": form,
    })


def friends_list(request):
    friends = FriendProfile.objects.all()
    return render(request, "main/friends_list.html", {"friends": friends})


def friend_detail(request, slug):
    friend = get_object_or_404(
        FriendProfile.objects.prefetch_related("photos"), slug=slug
    )
    return render(request, "main/friend_detail.html", {"friend": friend})
