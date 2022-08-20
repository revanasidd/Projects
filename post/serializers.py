from rest_framework import serializers
from django.contrib.auth.models import User
from post.models import *

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name','last_name','email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            # validated_data["first_name"],
            # validated_data["last_name"],
            validated_data['email'],
            validated_data['password']
            )
        return user

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title','description','image','liked_by','created_by')

    def create(self, validated_data):
        user = self.context['request'].user
        title = validated_data.pop('title',None)
        description = validated_data.pop('description',None)
        image = validated_data.pop('image',None)
        if title is None:
            raise serializers.ValidationError({"error":"title should be provided"})
        if description is None:
            raise serializers.ValidationError({"error":"description should be provided"})
        if image is None:
            raise serializers.ValidationError({"error":"image should be provided"})
        else:
            post = Post()
            post.title = title
            post.description = description
            post.image = image
            post.created_by = user
            post.save()
            return post
class PostSerializers(serializers.ModelSerializer):
    # liked_count = serializers.SerializerMethodField()
    # liked_by = serializers.SerializerMethodField()
    # image = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = '__all__'