from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage


def user_profile_image_path(instance, filename):
    return f'profile_images/user_{instance.user.id}/{filename}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to=user_profile_image_path, default='default.jpg')
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    county = models.CharField(max_length=100, blank=True)
    eir_code = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        old_image = None

        if self.pk:
            try:
                old_profile = UserProfile.objects.get(pk=self.pk)
                old_image = old_profile.profile_image
            except UserProfile.DoesNotExist:
                pass

        super().save(*args, **kwargs)

        if (
            old_image and
            old_image.name != 'default.jpg' and
            old_image.name != self.profile_image.name and
            default_storage.exists(old_image.name)
        ):
            try:
                old_image.delete(save=False)
            except Exception as e:
                print(f"Failed to delete old image: {e}")

    def __str__(self):
        return f"{self.user.username}'s Profile"