from django.shortcuts import render
from rest_framework import generics, permissions , mixins, status
from .models import Post, Vote
from .serializers import PostSerializer, VoteSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response 

# Create your views here.

class PostList(
    generics.ListCreateAPIView):  # ListCreateAPiView also hepls to post API in db, ListApiView only listout api, but ListCreateApi also support POST request
    queryset = Post.objects.all()  # what we are pulling from database / models
    serializer_class = PostSerializer  # which serializer we use for this Post
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]  # users can only see posts without registration/login,!! but to post the post you need to login hahaah MagicLOL!! (List of different permissions)

    def perform_create(self,  # executed just before saving to db
                       serializer):  # automatically called before our post is created to make poster as current user
        serializer.save(poster=self.request.user)



class PostRetrieveDestroy(   #for destroying post
    generics.RetrieveDestroyAPIView): 
    queryset = Post.objects.all()  # what we are pulling from database / models
    serializer_class = PostSerializer  # which serializer we use for this Post
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]  # users can only see posts without registration/login,!! but to post the post you need to login hahaah MagicLOL!! (List of different permissions)

    def delete(self,request,*args,**kwargs):
        post=Post.objects.filter(pk=kwargs['pk'],poster=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('This is\'t your post to delete BRUHH!!')

class VoteCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]  # List of different permissions

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Vote.objects.filter(voter=user, post=post)

    def perform_create(self, serializer):
        if self.get_queryset().exists():  # if there already exists the vote for the post by this user
            raise ValidationError('You have already voted for this post')

        serializer.save(voter=self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))
 

    def delete(self, request, *args,**kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('You never voted for this post ...silly!!')


