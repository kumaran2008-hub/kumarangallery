from django import forms
from django.contrib import admin

from .models import (
    ContactMessage,
    FriendPhoto,
    FriendProfile,
    GalleryCategory,
    GalleryImage,
)


class GalleryCategoryAdminForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput,
        help_text="Set a password. Leave blank when editing to keep the current one.",
    )

    class Meta:
        model = GalleryCategory
        fields = ["name", "slug", "password"]

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password and not self.instance.pk:
            raise forms.ValidationError("A password is required for a new category.")
        return password

    def save(self, commit=True):
        category = super().save(commit=False)
        raw_password = self.cleaned_data.get("password")
        if raw_password:
            category.set_password(raw_password)
        if commit:
            category.save()
            self.save_m2m()
        return category


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1


class FriendPhotoInline(admin.TabularInline):
    model = FriendPhoto
    extra = 1


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    form = GalleryCategoryAdminForm
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}
    inlines = [GalleryImageInline]


@admin.register(FriendProfile)
class FriendProfileAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}
    inlines = [FriendPhotoInline]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name", "email", "message"]
    readonly_fields = ["name", "email", "message", "created_at"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False
