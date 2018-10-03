from django.db import models
from django.core.exceptions import ValidationError


class Color(models.Model):
    R = models.IntegerField(default=255)
    G = models.IntegerField(default=0)
    B = models.IntegerField(default=0)

    def __str__(self):
        return str(self.R) + "\n" + str(self.G) + "\n" + str(self.B)

    # Only allow one of each
    def save(self, *args, **kwargs):
        if Color.objects.exists() and not self.pk:

            raise ValidationError("There is can be only one Color instance")
        return super(Color, self).save(*args, **kwargs)
