from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from post.serializers import *
from post.models import *
from django.contrib.auth import login
from rest_framework.permissions import (AllowAny,IsAuthenticated,IsAdminUser)
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
    GenericAPIView,
)
from rest_framework.views import APIView


# Register API
class RegisterAPI(generics.GenericAPIView):
    permission_classes =(AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

#Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

class PostCreateView(CreateAPIView):
    serializer_class = PostCreateSerializer
    permission_classes =(permissions.IsAuthenticated, )
    queryset = Post.objects.all()


class FallowUser(APIView):
    queryset = Followed.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = None

    def post(self,request):
        user = self.request.user
        user_id = self.request.data.get("user_id")
        user_obj = User.objects.filter(pk=user_id).last()
        followd_objs = Followed.objects.filter(user=user).last()
        if followd_objs:
            if user_obj in followd_objs.friends.all():
                return Response({"message":f"your already following {user_obj.username}"})
            else:
                followd_objs.friends.add(user_obj)
                followd_objs.save()
                return Response({"message":f"Your succesfully following this {user_obj.username}"})
        else:
            followed_obj = Followed.objects.create(user=user)
            followed_obj.friends.add(user_obj)
            followed_obj.save()
            followed_obj = Followed.objects.create(user=user_obj)
            followed_obj.friends.add(user)
            followed_obj.save()
            return Response({"message":f"Your succesfully following this {user_obj.username}"})

class UserLikedPost(APIView):
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = None

    def post(self,request):
        user = self.request.user
        post_id = self.request.data.get("post_id")
        post_obj = Post.objects.filter(pk=post_id).last()
        if post_obj:
            if user not in post_obj.liked_by.all():
                post_obj.liked_by.add(user)
                post_obj.save()
                return Response({"message":f"you liked this post {post_obj.title}"})
            else:
                post_obj.liked_by.remove(user)
                post_obj.save()
                return Response({"message":f"You unliked this post {post_obj.title}"})
        else:
            return Response({"message":"You try to like the post not existed"})

class PostLists(ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = None

    def get(self,request):
        user = self.request.user
        print(f'103-------',user)
        user_id = self.request.data.get("user_id")
        print(f'105---------',user_id)
        user_obj = User.objects.filter(pk=user_id).last()
        follwers_objs = Followed.objects.filter(user=user_obj).last()
        print(f'106-------------',follwers_objs)
        if follwers_objs:
            print(f'110-------{user}-----------{follwers_objs.friends.all()}-')
            if user in follwers_objs.friends.all():
                print(f'112--------',user)
                post_objs = Post.objects.filter(created_by=user_obj)
                if post_objs:
                    print(f'109-------------',post_objs)
                    serializer_data = PostSerializers(post_objs,many=True).data
                    return Response({"posts":serializer_data})
                else:
                    return Response({"message":"No Posts added "})
            else:
                return Response({"message":"Your Not following"})
        else:
            return Response({"message":"Your not following this user So you cant see his posts"})



