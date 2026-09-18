from django.urls import path
from . import views


urlpatterns = [

    # =====================================================
    # PRACTICAL 8 - ADVANCED ORM QUERIES
    # =====================================================

    path(
        "advanced/",
        views.advanced_queries,
        name="advanced_queries"
    ),

    # =====================================================
    # MESSAGE LIST
    # =====================================================

    path(
        "",
        views.message_list,
        name="message_list"
    ),

    # =====================================================
    # PRACTICAL 9 - ROLE BASED ACCESS
    # =====================================================

    path(
        "editor/",
        views.editor_dashboard,
        name="editor_dashboard"
    ),

    path(
        "viewer/",
        views.viewer_dashboard,
        name="viewer_dashboard"
    ),

    # =====================================================
    # CREATE POST
    # =====================================================

    path(
        "post/create/",
        views.post_create,
        name="post_create"
    ),

    path(
        "post/success/",
        views.post_success,
        name="post_success"
    ),

    # =====================================================
    # PRACTICAL 10 - SEARCH AND FILTER
    # =====================================================

    path(
        "search/",
        views.search_messages,
        name="search_messages"
    ),

    # =====================================================
    # PRACTICAL 11 - PAGINATION
    # =====================================================

    path(
        "pagination/",
        views.paginated_messages,
        name="paginated_messages"
    ),

    # =====================================================
    # PRACTICAL 12 - DASHBOARD
    # =====================================================

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    # =====================================================
    # PRACTICAL 13 - DOCUMENT UPLOAD
    # =====================================================

    path(
        "documents/upload/",
        views.document_upload,
        name="document_upload"
    ),

    path(
        "documents/",
        views.document_list,
        name="document_list"
    ),

    path(
        "documents/delete/<int:document_id>/",
        views.document_delete,
        name="document_delete"
    ),

    # =====================================================
    # PRACTICAL 14 - EXPORT CSV
    # =====================================================

    path(
        "export/csv/",
        views.export_messages_csv,
        name="export_messages_csv"
    ),

    # =====================================================
    # PRACTICAL 15 - BASIC JSON API
    # =====================================================

    path(
        "api/messages/",
        views.messages_api,
        name="messages_api"
    ),

]