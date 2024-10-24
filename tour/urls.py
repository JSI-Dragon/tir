from django.urls import path
from .views import BannerIndexView, BannerDetailView, TourListView, TourSeasonView, FeedbackListView, TourSearchView, \
    RegionTourListView, RegionTourDetailView, TourDetailView

urlpatterns = [
    path('banners/', BannerIndexView.as_view(), name='banner-list-create'),
    path('banners/<int:pk>/', BannerDetailView.as_view(), name='banner-detail'),
    path('tours/', TourListView.as_view(), name='tour-list'),
    path('tours/season/', TourSeasonView.as_view(), name='tour-season'),
    path('feedbacks/', FeedbackListView.as_view(), name='feedback-list'),
    path('tours/search/', TourSearchView.as_view(), name='tour-search'),
    path('regions/', RegionTourListView.as_view(), name='region-list'),
    path('regions/<int:pk>/', RegionTourDetailView.as_view(), name='region-detail'),
    path('tours/<int:id>/', TourDetailView.as_view(), name='tour-detail'),

]
