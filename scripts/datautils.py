from faker import Faker
from main.models import Blog

# Generate 500 blog entries using Faker
faker = Faker()

for _ in range(0, 500):
    Blog.objects.create(title=faker.sentence(), body=faker.paragraph())
