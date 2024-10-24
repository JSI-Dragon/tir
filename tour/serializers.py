from django.db.models import Avg
from rest_framework import serializers
from .models import Banner, Tour, Feedback, Rating, RegionTour


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['title', 'banner_image']


class RegionTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionTour
        fields = ['title', 'description', 'slug', 'image']


class TourSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    date_tour = RegionTourSerializer(many=True)

    class Meta:
        model = Tour
        fields = ['title', 'description', 'images', 'price', 'average_rating', 'date_tour']

    def get_average_rating(self, obj):
        return obj.ratings.aggregate(average=Avg('score'))['average'] or None


class FeedbackSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = ['user_name', 'comment', 'children']

    def get_children(self, obj):
        # Используем "self" для рекурсивного вызова сериализатора
        return FeedbackSerializer(obj.children.all(), many=True).data if obj.children.exists() else None


class DetailSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()  # Для вычисления среднего рейтинга

    class Meta:
        model = Tour
        fields = ['title',
                  'description',
                  'image',
                  'start_date',
                  'end_date',
                  'rating',
                  'participants_price',
                  'max_participants']

    def get_rating(self, obj):
        # Получаем средний рейтинг из модели Rating, связанной с туром
        average_rating = obj.ratings.aggregate(Avg('score'))['score__avg']
        return average_rating if average_rating is not None else 0  # Возвращаем 0, если нет рейтингов

