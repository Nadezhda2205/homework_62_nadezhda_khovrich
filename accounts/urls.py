from django.urls import path
from accounts.view import LoginView, logout_view, RegisterView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    # path(r'^login/$', LoginView.as_view(), name='login'),
    # r'^search/$'

    path('logout/', logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]
