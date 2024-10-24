from rest_framework import serializers
from .models import MyUser
from tour.models import Tour, Booking

class MyUserSerializer(serializers.ModelSerializer):
    favorite_tours = serializers.StringRelatedField(many=True)
    bookings = serializers.StringRelatedField(many=True)

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'favorite_tours', 'bookings'] 


class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ['title', 'description', 'price', 'duration', 'start_date', 'end_date']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'tour', 'date', 'status', 'total_price']


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, error_messages={
        'min_length': 'Пароль должен содержать не менее 8 символов.'
    })
    email = serializers.EmailField(required=True)

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password']

    def create(self, validated_data):

        user = MyUser(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserProfileListSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'avatar']

    def validate_avatar(self, value):

        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Размер аватара не должен превышать 2MB.")
        return value
    
class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'username', 'email', 'status', 'is_blocked']
