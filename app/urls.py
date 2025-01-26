from django.urls import path
from .views import IndexView, LoginView, LogoutView, ProfileView, StudentsView
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('students/', StudentsView.as_view(), name='students'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
