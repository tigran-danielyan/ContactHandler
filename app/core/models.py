from datetime import timedelta

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone


class Contact(models.Model):
    """
    Name
    Phone Number
    Email Address
    """

    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        acceptable_time = timezone.now() - timedelta(minutes=settings.ACCEPTABLE_TIME_FOR_CREATING)
        contact_obj = Contact.objects.filter(Q(email=self.email, created_at__gte=acceptable_time) |
                                             Q(phone_number=self.phone_number, created_at__gte=acceptable_time))

        if contact_obj:
            raise ValueError("contact with this email/phone is created minutes before")

        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'{self.name}-{self.phone_number}-{self.email}'
