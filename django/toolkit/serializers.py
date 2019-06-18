from rest_framework import serializers


class ScoreSerializer(serializers.Serializer):

    axis = serializers.IntegerField()
    domain = serializers.IntegerField()
    question = serializers.IntegerField()
    answer = serializers.IntegerField()
    value = serializers.IntegerField()
