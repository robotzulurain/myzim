from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = "Create or update a superuser from DJANGO_SUPERUSER_* env vars"

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        if not username or not password:
            self.stdout.write("DJANGO_SUPERUSER_USERNAME or DJANGO_SUPERUSER_PASSWORD not set")
            return
        u, created = User.objects.get_or_create(username=username, defaults={'email': email})
        u.is_superuser = True
        u.is_staff = True
        u.set_password(password)
        u.save()
        self.stdout.write(f"superuser {'created' if created else 'updated'}: {username}")
