from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('register/', views.register, name='register'),
    path('create-quotation/', views.create_project, name='create_quotation'),
    path('project_list/', views.project_list, name='project_list'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('admin/projects/update/<int:project_id>/', views.update_project, name='update_project'),
    path('admin/projects/remove_element/<int:element_id>/', views.remove_project_element,
         name='remove_project_element'),
    path('admin/projects/remove_material/<int:material_id>/', views.remove_material, name='remove_material'),
    path('approve-project/<int:project_id>/', views.approve_project, name='approve_project')
]

