from django.db import models

from accounts.models import User



# Create your models here.


from facility.models import Department, Location

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    phone = models.CharField(max_length=15, null=True)
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"


