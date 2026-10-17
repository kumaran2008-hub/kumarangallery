from django.contrib.auth.hashers import check_password, make_password
from django.db import models


class GalleryCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    password = models.CharField(max_length=128)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "gallery categories"

    def __str__(self):
        return self.name

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class GalleryImage(models.Model):
    category = models.ForeignKey(
        GalleryCategory, on_delete=models.CASCADE, related_name="images"
    )
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to="gallery/")

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class FriendProfile(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    dp = models.ImageField(upload_to="friends/profiles/")
    story = models.TextField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class FriendPhoto(models.Model):
    friend = models.ForeignKey(
        FriendProfile, on_delete=models.CASCADE, related_name="photos"
    )
    image = models.ImageField(upload_to="friends/photos/")
    caption = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.caption or f"Photo of {self.friend.name}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Message from {self.name} ({self.created_at:%Y-%m-%d})"
