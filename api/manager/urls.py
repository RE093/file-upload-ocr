from django.contrib import admin
from django.urls import path
from manager.views import UploadFileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload', UploadFileView.as_view({'post': 'create'}))
]
