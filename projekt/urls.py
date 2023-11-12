from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('model', GetModel, basename='model')
router.register('expert', GetExperts, basename='expert')
router.register('model_expert', GetModelExpert, basename='model_expert')
router.register('criterias', GetCriterias, basename='criterias')
router.register('model_criterias', GetModelCriterias, basename='model_criterias')
router.register('weight_criterias', GetWeightsCriterias, basename='weight_criterias')
router.register('data_elements', GetDataElements, basename='data_elements')
router.register('matrices', GetMatrices, basename='matrices')
router.register('matrice_elements', GetMatriceElements, basename='matrice_elements')
router.register('data_matrices', GetDataMatrices, basename='data_matrices')
router.register('decision_scenarios', GetDecisionScenarios, basename='decision_scenarios')
urlpatterns = router.urls