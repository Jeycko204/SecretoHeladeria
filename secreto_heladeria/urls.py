from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from compras.views import UserLoginView, AdminLoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("", views.home_view, name="home"),
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('admin/login/', AdminLoginView.as_view(), name='admin_login'),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('compras/', include('compras.urls')),
    path('api/', include('compras.urls_api')),
    path('api-auth/', include('rest_framework.urls')), # Login para Browsable API
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("admin/", admin.site.urls),
]
