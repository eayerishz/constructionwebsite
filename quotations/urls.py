from django.urls import path
from . import views
from django.contrib import admin
from quotations.views import home, login_view
from .views import user_logout

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('create_project/', views.create_project, name='create_project'),
    path('project_list/', views.project_list, name='project_list'),
    path('login/', login_view, name='login'),
    path('logout/', user_logout, name='logout'),
]


