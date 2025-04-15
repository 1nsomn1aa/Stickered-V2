from django.db import models


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    role = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name