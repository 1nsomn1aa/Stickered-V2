from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ExifTags
import os


def user_profile_image_path(instance, filename):
    return f'profile_images/user_{instance.user.id}/{filename}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to=user_profile_image_path, default='default.jpg')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        image_path = self.profile_image.path
        if self.profile_image and self.profile_image.name != 'default.jpg' and os.path.isfile(image_path):
            try:
                img = Image.open(image_path)

                try:
                    exif = img._getexif()
                    if exif:
                        orientation = next(k for k, v in ExifTags.TAGS.items() if v == 'Orientation')
                        orientation_value = exif.get(orientation)
                        if orientation_value == 3:
                            img = img.rotate(180, expand=True)
                        elif orientation_value == 6:
                            img = img.rotate(270, expand=True)
                        elif orientation_value == 8:
                            img = img.rotate(90, expand=True)
                except Exception:
                    pass

                if img.height > 300 or img.width > 300:
                    img.thumbnail((300, 300))

                img.save(image_path)

            except Exception as e:
                print(f"Image processing failed: {e}")

    def __str__(self):
        return f"{self.user.username}'s Profile"
