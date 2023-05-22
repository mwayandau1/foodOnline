from django.urls import path, include
from .import views
from accounts import views as AccountsViews

urlpatterns =[
    path('', AccountsViews.venDashboard, name='vendor'),
    path('profile/', views.ven_profile, name='ven_profile'),
]