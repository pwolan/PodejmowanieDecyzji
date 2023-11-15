from .views import *
from django.urls import path, include
from django.contrib.auth import views as auth_views
# from rest_framework.routers import DefaultRouter
from . import views

# router = DefaultRouter()
# router.register('model', GetModel, basename='model')
# router.register('expert', GetExperts, basename='expert')
# router.register('model_expert', GetModelExpert, basename='model_expert')
# router.register('criterias', GetCriterias, basename='criterias')
# router.register('model_criterias', GetModelCriterias, basename='model_criterias')
# router.register('weight_criterias', GetWeightsCriterias, basename='weight_criterias')
# router.register('data_elements', GetDataElements, basename='data_elements')
# router.register('matrices', GetMatrices, basename='matrices')
# router.register('matrice_elements', GetMatriceElements, basename='matrice_elements')
# router.register('data_matrices', GetDataMatrices, basename='data_matrices')
# router.register('decision_scenarios', GetDecisionScenarios, basename='decision_scenarios')
# router.register('decision_scenario', DecisionScenario, basename='decision_scenario')
new_urls = [
    path("", views.index, name="index"),
    path("accounts/login/", views.MyLoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('add_decision_scenario/', views.ScenarioFormView.as_view())
]
urlpatterns = new_urls