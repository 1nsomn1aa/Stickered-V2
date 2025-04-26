from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage


def user_profile_image_path(instance, filename):
    return f'profile_images/user_{instance.user.id}/{filename}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to=user_profile_image_path, default='default.jpg')

    def save(self, *args, **kwargs):
        if self.pk:
            old_profile = UserProfile.objects.get(pk=self.pk)
            old_image = old_profile.profile_image
        else:
            old_image = None

        super().save(*args, **kwargs)

        if self.profile_image and self.profile_image.name != 'default.jpg' and old_image and old_image != self.profile_image:
            try:
                if old_image:
                    old_image.delete(save=False)
            except Exception as e:
                print(f"Failed to delete old image: {e}")

    def __str__(self):
        return f"{self.user.username}'s Profile"
