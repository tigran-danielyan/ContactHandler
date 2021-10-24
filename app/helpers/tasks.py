from django.db import transaction
from contact_processor import celery_app
from core.models import Contact


@celery_app.task(bind=True, acks_late=True)
def create_new_contact(self, contact_list):
    with transaction.atomic():

        for contact in contact_list:
            obj = Contact(**contact)
            try:
                obj.save()
            except ValueError:
                pass
