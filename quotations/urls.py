from django.urls import path
from . import views
from django.contrib import admin
from quotations.views import home, login_view, project_detail, create_project
from .views import user_logout, approve_project

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('create-quotation/', create_project, name='create_quotation'),
    path('project_list/', views.project_list, name='project_list'),
    path('projects/<int:project_id>/', project_detail, name='project_detail'),  # Now it should work
    path('login/', login_view, name='login'),
    path('logout/', user_logout, name='logout'),
    path('approve-project/<int:project_id>/', approve_project, name='approve_project')
]