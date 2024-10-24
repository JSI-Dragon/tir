from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('profile/bookings/', views.UserBookingsView.as_view(), name='user-bookings'),
    path('api/user/bookings/<int:booking_id>/', views.UserBookingsView.as_view(), name='cancel-booking'),
    path('profile/tours/create/', views.UserTourCreationView.as_view(), name='create-tour'),  # Эндпоинт для создания тура
    path('profile/tours/<int:tour_id>/edit/', views.UserTourCreationView.as_view(), name='edit-tour'),
    path('profile/withdraw/', views.UserWithdrawFundsView.as_view(), name='withdraw-funds'),
    path('admin/users/', views.AdminUserListView.as_view(), name='admin-user-list'),
    path('admin/users/<int:user_id>/block/', views.AdminUserBlockView.as_view(), name='admin-user-block'),
    path('admin/users/<int:user_id>/delete/', views.AdminUserDeleteView.as_view(), name='admin-user-delete'),
    path('admin/tours/<int:tour_id>/delete/', views.TourModerationView.as_view(), name='admin-tour-delete'),
    path('admin/tours/<int:tour_id>/block/', views.TourModerationView.as_view(), name='admin-tour-block'),
    path('admin/statistics/', views.AdminStatisticsView.as_view(), name='admin-statistics'),
]

