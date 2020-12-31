from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
urlpatterns = [
	path('',views.homepage,name='homepage'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('login/availability/',views.availability,name='availability'),
    path('adminpage/',views.adminpage,name='adminpage'),
    path('login/myroster/',views.myroster,name='myroster'),
    #password reset paths
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='accounts/reset_password.html'),name='reset_password'),

    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='accounts/reset_password_sent.html'),name='password_reset_done'),
    
    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),name='password_reset_confirm'),
    
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),name='password_reset_complete'),
    
]
