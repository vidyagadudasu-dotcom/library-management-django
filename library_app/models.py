from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateField()
    available = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField(default=1)  # 👈 ADD THIS
    def __str__(self):
        return self.title

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    roll_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class IssueBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(default=timezone.now)
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Only when issuing the book for the first time
        if not self.pk:
            if self.book.quantity <= 0:
                raise ValidationError("This book is not available")

            self.book.quantity -= 1

            if self.book.quantity == 0:
                self.book.available = False

            self.book.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.book}"