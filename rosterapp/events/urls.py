from django.urls import path
from .import views
from accounts import views as accounts_views
urlpatterns = [
    path('adminpage/createroster/', views.roster,name='roster'),
    path('adminpage/viewroster/',views.viewroster,name='viewroster'),
    path('createallevents/',views.allevents,name='allevents'),
    path('createextraevents/',views.createextraevents,name='createextraevents'),
    path('availability/swap/',views.swap,name='swap'),
    path('adminpage/createaccount/',accounts_views.createaccount,name='createaccount'),
    path('login/currentteam',views.currentteam,name='currentteam'),
 #   path('adminpage/viewroster2/',views.viewroster,name = 'viewroster2'),
]
