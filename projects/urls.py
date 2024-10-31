
from django.contrib import admin
from django.urls import path,include
from .views import admin_dashboard, project_detail, add_material, update_material, remove_material
from .views import approve_project, user_approve_project, decline_project, complete_project
urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/project/<int:project_id>/', project_detail, name='project_detail'),
    path('admin/project/<int:project_id>/add_material/', add_material, name='add_material'),
    path('admin/project/update_material/<int:material_id>/', update_material, name='update_material'),
    path('admin/project/<int:project_id>/remove_material/<int:material_id>/', remove_material, name='remove_material'),
    path('admin/project/<int:project_id>/approve/', approve_project, name='approve_project'),
    path('user/project/<int:project_id>/approve/', user_approve_project, name='user_approve_project'),
    path('user/project/<int:project_id>/decline/', decline_project, name='decline_project'),
    path('admin/project/<int:project_id>/complete/', complete_project, name='complete_project'),
]