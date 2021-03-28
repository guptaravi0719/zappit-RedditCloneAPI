from rest_framework import serializers
from .models import Post,Vote


class PostSerializer(serializers.ModelSerializer):  # serializes(translates) the models to json
    class Meta:
        model = Post  # which model it refers ?
        fields = ['id', 'title', 'url', 'poster', 'created','poster_id','votes']

    poster = serializers.ReadOnlyField(source='poster.username')
    poster_id = serializers.ReadOnlyField(source='poster.id')
    votes = serializers.SerializerMethodField()  #now it will look for method named get_(variablename) in this class and assign the return value to it . LOL

    def get_votes(self,post):
        return Vote.objects.filter(post=post).count()
    


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id']

