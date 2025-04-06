from django.urls import path, include
from .views import RegisterView, LoginView, ProfileView, UserSearchView, UpdateUserView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('profile/', UpdateUserView, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('user-search/', UserSearchView.as_view(), name='user-search'),
    # path('update-user/', UpdateUserView.as_view(), name='update-user'),
    path('update-user/', UpdateUserView.as_view({'post': 'update-user'}), name='update-user'),
]