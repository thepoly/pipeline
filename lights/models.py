from django.db import models
from django.core.exceptions import ValidationError


class Color(models.Model):
    R = models.IntegerField(default=255)
    G = models.IntegerField(default=0)
    B = models.IntegerField(default=0)
    id = models.IntegerField(primary_key=True, default=0, editable=False)

    def __str__(self):
        return str(self.R) + "\n" + str(self.G) + "\n" + str(self.B)
