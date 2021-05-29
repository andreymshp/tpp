from django.urls import path
from . import views

app_name = "requ"
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.detail, name='detail'),
    path('<int:id>/comment', views.comment, name='comment'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('sysadmin/', views.admin, name='admin'),
    path('user/', views.user, name='user'),
    path('profile/', views.profile, name="profile"),
    path('<int:id>/solved', views.solved, name="solved"),
    path('back/', views.back, name="back"),
    path('new_request', views.new_request, name="new_request"),
    path('<int:id>/unsolved', views.unsolved, name="unsolved"),
]
