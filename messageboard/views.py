from django.shortcuts import render, redirect
from .models import Message, Post, Document
from .forms import PostForm, DocumentForm
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required, user_passes_test


# =========================================================
# PRACTICAL 8 - ADVANCED ORM QUERIES
# =========================================================

@login_required
def advanced_queries(request):

    total_messages = Message.objects.count()

    all_messages = Message.objects.all()

    priya_messages = Message.objects.filter(
        name__icontains="Priya"
    )

    gmail_messages = Message.objects.filter(
        email__icontains="gmail.com"
    )

    hello_messages = Message.objects.filter(
        message__icontains="hello"
    )

    latest_messages = Message.objects.all().order_by(
        "-created_at"
    )

    return render(
        request,
        "messageboard/advanced_queries.html",
        {
            "total_messages": total_messages,
            "all_messages": all_messages,
            "priya_messages": priya_messages,
            "gmail_messages": gmail_messages,
            "hello_messages": hello_messages,
            "latest_messages": latest_messages,
        }
    )


# =========================================================
# MESSAGE LIST
# =========================================================

@login_required
def message_list(request):

    messages = Message.objects.all().order_by("-created_at")

    return render(
        request,
        "messageboard/message_list.html",
        {
            "messages": messages
        }
    )


# =========================================================
# POST CREATE
# =========================================================

def post_create(request):

    if request.method == "POST":

        form = PostForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("post_success")

    else:

        form = PostForm()

    return render(
        request,
        "messageboard/post_form.html",
        {
            "form": form
        }
    )


# =========================================================
# POST SUCCESS
# =========================================================

def post_success(request):

    return render(
        request,
        "messageboard/post_success.html"
    )


# =========================================================
# PRACTICAL 9 - ROLE BASED ACCESS
# =========================================================

def is_editor(user):

    return user.groups.filter(
        name="Editor"
    ).exists()


def is_viewer(user):

    return user.groups.filter(
        name="Viewer"
    ).exists()


# ---------------------------------------------------------
# EDITOR PAGE
# ---------------------------------------------------------

@login_required
@user_passes_test(is_editor)
def editor_dashboard(request):

    return render(
        request,
        "messageboard/editor_dashboard.html"
    )


# ---------------------------------------------------------
# VIEWER PAGE
# ---------------------------------------------------------

@login_required
@user_passes_test(is_viewer)
def viewer_dashboard(request):

    return render(
        request,
        "messageboard/viewer_dashboard.html"
    )


# =========================================================
# PRACTICAL 10 - SEARCH AND FILTER
# =========================================================

@login_required
def search_messages(request):

    search = request.GET.get("search", "")
    domain = request.GET.get("domain", "")

    messages = Message.objects.all().order_by("-created_at")

    if search:

        messages = messages.filter(
            name__icontains=search
        ) | messages.filter(
            email__icontains=search
        ) | messages.filter(
            message__icontains=search
        )

    if domain == "gmail":

        messages = messages.filter(
            email__icontains="@gmail.com"
        )

    elif domain == "yahoo":

        messages = messages.filter(
            email__icontains="@yahoo.com"
        )

    elif domain == "outlook":

        messages = messages.filter(
            email__icontains="@outlook.com"
        )

    return render(
        request,
        "messageboard/search_messages.html",
        {
            "messages": messages,
            "search": search,
            "domain": domain,
        }
    )


# =========================================================
# PRACTICAL 11 - PAGINATION
# =========================================================

@login_required
def paginated_messages(request):

    messages = Message.objects.all().order_by("-created_at")

    paginator = Paginator(messages, 5)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "messageboard/paginated_messages.html",
        {
            "page_obj": page_obj
        }
    )


# =========================================================
# PRACTICAL 12 - DASHBOARD STATISTICS
# =========================================================

@login_required
def dashboard(request):

    total_messages = Message.objects.count()

    gmail_messages = Message.objects.filter(
        email__icontains="@gmail.com"
    ).count()

    yahoo_messages = Message.objects.filter(
        email__icontains="@yahoo.com"
    ).count()

    outlook_messages = Message.objects.filter(
        email__icontains="@outlook.com"
    ).count()

    latest_messages = Message.objects.all().order_by(
        "-created_at"
    )[:5]

    return render(
        request,
        "messageboard/dashboard.html",
        {
            "total_messages": total_messages,
            "gmail_messages": gmail_messages,
            "yahoo_messages": yahoo_messages,
            "outlook_messages": outlook_messages,
            "latest_messages": latest_messages,
        }
    )


# =========================================================
# PRACTICAL 13 - DOCUMENT UPLOAD
# =========================================================

@login_required
def document_upload(request):

    if request.method == "POST":

        form = DocumentForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect("document_list")

    else:

        form = DocumentForm()

    return render(
        request,
        "messageboard/document_upload.html",
        {
            "form": form
        }
    )


# =========================================================
# PRACTICAL 13 - DOCUMENT LIST
# =========================================================

@login_required
def document_list(request):

    documents = Document.objects.all().order_by("-uploaded_at")

    return render(
        request,
        "messageboard/document_list.html",
        {
            "documents": documents
        }
    )
# =========================================================
# PRACTICAL 13 - DELETE DOCUMENT
# =========================================================

@login_required
def document_delete(request, document_id):

    document = Document.objects.get(id=document_id)

    if request.method == "POST":

        document.file.delete()

        document.delete()

        return redirect("document_list")

    return render(
        request,
        "messageboard/document_confirm_delete.html",
        {
            "document": document
        }
    )
# =========================================================
# PRACTICAL 14 - EXPORT MESSAGES TO CSV
# =========================================================

import csv
from django.http import HttpResponse


@login_required
def export_messages_csv(request):

    messages = Message.objects.all().order_by("-created_at")

    response = HttpResponse(
        content_type="text/csv"
    )

    response["Content-Disposition"] = (
        'attachment; filename="messages.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        "ID",
        "Name",
        "Email",
        "Message",
        "Created At"
    ])

    for message in messages:

        writer.writerow([
            message.id,
            message.name,
            message.email,
            message.message,
            message.created_at
        ])

    return response
# =========================================================
# PRACTICAL 15 - BASIC JSON API
# =========================================================

from django.http import JsonResponse


@login_required
def messages_api(request):

    messages = Message.objects.all().order_by("-created_at")

    data = []

    for message in messages:

        data.append({
            "id": message.id,
            "name": message.name,
            "email": message.email,
            "message": message.message,
            "created_at": message.created_at,
        })

    return JsonResponse({
        "messages": data
    })