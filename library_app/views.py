from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student, IssueBook
from django.http import HttpResponse
from django.core.management import call_command

def student_login(request):
    if request.method == "POST":
        email = request.POST.get("email").strip()
        roll_number = request.POST.get("roll_number").strip()

        try:
            student = Student.objects.get(
                email=email,
                roll_number=roll_number
            )
            request.session["student_email"] = student.email
            return redirect("/dashboard/")
        except Student.DoesNotExist:
            messages.error(request, "Invalid email or roll number")

    return render(request, "login.html")


def student_dashboard(request):
    student_email = request.session.get("student_email")

    if not student_email:
        return redirect("/login/")

    student = Student.objects.get(email=student_email)
    issued_books = IssueBook.objects.filter(student=student)

    return render(request, "dashboard.html", {
        "student": student,
        "issued_books": issued_books
    })


def student_logout(request):
    request.session.flush()
    return redirect("/login/")


# Temporary view to run migrations on Render
def run_migrations(request):
    call_command("migrate")
    return HttpResponse("Migrations applied successfully!")