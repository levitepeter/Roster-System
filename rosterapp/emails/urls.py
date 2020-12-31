from django.urls import path
from .import views
urlpatterns = [
    path('adminpage/sendmail',views.test_email,name='test_email'),
    
]
