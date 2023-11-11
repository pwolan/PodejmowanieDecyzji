from rest_framework import serializers
from .models.models  import*

class ModelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Models
        fields = "__all__"
class ExpertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experts
        fields = "__all__"
class ModelExpertSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelExperts
        fields = "__all__"