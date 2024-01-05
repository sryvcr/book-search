from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=150, unique=True, blank=False, null=False)

    def __str__(self):
        return f"{self.pk} - {self.name}"


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)

    def __str__(self):
        return f"{self.pk} - {self.name}"


class Book(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    subtitle = models.CharField(max_length=200, blank=False, null=False)
    author = models.ManyToManyField(Author, related_name="book", db_index=False)
    category = models.ManyToManyField(
        Category, related_name="book", db_index=False
    )
    publication_date = models.DateField(blank=False, null=False)
    editor = models.CharField(max_length=150, blank=False, null=False)
    description = models.TextField(null=False)
    image = models.CharField(blank=True, null=True)

    @property
    def authors(self):
        return self.author.all()

    @property
    def categories(self):
        return self.category.all()

    def __str__(self):
        return f"{self.pk} - {self.title}"
