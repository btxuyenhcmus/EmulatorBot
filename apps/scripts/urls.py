from django.urls import path
from . import views
urlpatterns = [
    path('create-script/', views.create_script, name='create_script'),
    path('run/<int:script_id>', views.run_script,
         name='run_script'),
    path('fetch-scripts/', views.fetch_scripts, name='fetch_scripts'),
    path('delete-script/<int:script_id>',
         views.delete_script, name='delete_script'),
    path('fetch-script-by-id/<int:script_id>',
         views.get_script_by_id, name='fetch_script_by_id')
]
