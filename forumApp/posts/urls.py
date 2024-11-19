
from django.urls import path, include
from forumApp.posts.views import dashboard, add_post, delete_post, details_page, edit_post, Index, PostDetailView, \
    DashboardView, AddPostView, DeletePageView, approve_post

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('dashboard/', DashboardView.as_view(), name='dash'),
    path('add-post/', AddPostView.as_view(), name='add-post'),
    path('<int:pk>/', include([
        path('approve/', approve_post, name='approve-post'),
        path('delete-post/', DeletePageView.as_view(), name='delete-post'),
        path('details-post/', PostDetailView.as_view(), name='details-post'),
        path('edit-post/', edit_post, name='edit-post'),
    ]))
]
