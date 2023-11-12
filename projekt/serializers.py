from rest_framework import serializers
from .models.models  import*
from .models.weights import*
from .models.matrices import*
from .models.decisionScenarios import*

# serializers from models.py
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
class CriteriasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criterias
        fields = "__all__"
class ModelCriteriasSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelCriterias
        fields = "__all__"

#serializers from weights.py
class WeightsCriteriasSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightsCriterias
        fields = "__all__"
class DataElementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataElements
        fields = "__all__"

#serializers from matrices.py
class MatricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matrices
        fields = "__all__"
class MatriceElementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatriceElements
        fields = "__all__"
class DataMatricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataMatrices
        fields = "__all__"

#serializers from decisionScenarios.py
class DecisionScenariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = DecisionScenarios
        fields = "__all__"