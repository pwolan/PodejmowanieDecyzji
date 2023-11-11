from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('Model', GetModel, basename='model')
router.register('Expert', GetExperts, basename='expert')
router.register('ModelExpert', GetModelExpert, basename='modelExpert')
urlpatterns = router.urls