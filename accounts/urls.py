from django.urls import path
from accounts.view import LoginView, logout_view, RegisterView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('login/', logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
   
]
