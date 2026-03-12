from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect, get_object_or_404
from .models import Author, Book, Student, IssueBook

# Keep normal models registered
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Student)

# View to handle return button click
def return_book_view(request, issue_id):
    issue = get_object_or_404(IssueBook, id=issue_id)
    if not issue.is_returned:
        issue.is_returned = True
        issue.book.quantity += 1
        issue.book.available = True
        issue.book.save()
        issue.save()
    return redirect('/admin/library_app/issuebook/')  # replace library_app with your app name

# Custom admin class for IssueBook
@admin.register(IssueBook)
class IssueBookAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'issue_date', 'return_date', 'is_returned', 'return_button')
    readonly_fields = ('issue_date',)

    def return_button(self, obj):
        if not obj.is_returned:
            return format_html(
                '<a class="button" href="{}">Return</a>',
                f'/admin/library_app/issuebook/{obj.id}/return/'  # replace library_app with your app name
            )
        return "Returned"
    return_button.short_description = 'Return Book'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:issue_id>/return/', self.admin_site.admin_view(return_book_view), name='return-book'),
        ]
        return custom_urls + urls