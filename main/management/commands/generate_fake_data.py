from django.core.management.base import BaseCommand

from faker import Faker
from main.models import Blog, Comment, Category


class Command(BaseCommand):
    help = 'Generate blogs and comments fake data using Faker library'

    def handle(self, *args, **options):
        # Create Faker instance
        faker = Faker()

        # Generate categories
        Category.objects.create(name='Web development')
        Category.objects.create(name='Databases')
        Category.objects.create(name='Data science')
        Category.objects.create(name='Security')
        Category.objects.create(name='Django')
        Category.objects.create(name='Python')

        # Generate 500 blog entries
        for _ in range(0, 500):
            Blog.objects.create(title=faker.sentence(), body=faker.paragraph())

        # Generate 3 comments per blog entry
        for blog in Blog.objects.iterator():
            # Create the comment objects
            comments = [Comment(text=faker.paragraph(), blog=blog) for _ in range(0, 3)]

            # Builk create previous comments in the db
            Comment.objects.bulk_create(comments)
