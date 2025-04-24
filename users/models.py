from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os


def user_profile_image_path(instance, filename):
    return f'profile_images/user_{instance.user.id}/{filename}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to=user_profile_image_path, default='default.jpg')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_image and os.path.isfile(self.profile_image.path):
            image_path = self.profile_image.path
            img = Image.open(image_path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(image_path)

    def __str__(self):
        return f"{self.user.username}'s Profile"
