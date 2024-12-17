# generate_fake_posts.py

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils import timezone
from blog.models import Post  # Update with the correct import path
from django.contrib.auth.models import User
from faker import Faker
import random
import os

class Command(BaseCommand):
    help = 'Generate fake posts for testing purposes'

    def handle(self, *args, **kwargs):
        fake = Faker()
        num_posts = 20  # Number of fake posts to create

        # Get all users to assign as authors
        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.ERROR("No users found in the database. Create some users first."))
            return

        # Paths to sample images for bg_image and post_image fields
        bg_image_path = "images_fake/img1"      # Replace with your image path
        post_image_path = "images_fake/img2"  # Replace with your image path

        for _ in range(num_posts):
            title = fake.sentence(nb_words=6)
            slug = slugify(title)

            Post.objects.create(
                title=title,
                author=random.choice(users),
                slug=slug,
                body=fake.paragraph(nb_sentences=5),
                bg_image=bg_image_path,
                post_image=post_image_path,
                created_at=fake.date_time_this_year(),
                updated_at=timezone.now(),
                publish=timezone.now(),
                status=random.choice([Post.Status.DRAFT, Post.Status.PUBLISHED]),
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_posts} fake posts'))
