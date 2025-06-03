from django.urls import path

from .views import UserRegisterView, UserLoginView, UserLogoutView, UserProfileEditView

app_name = 'users'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/edit/', UserProfileEditView.as_view(), name='profile_edit'),
]
