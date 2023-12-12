from django.urls import path
from django.contrib.auth import views as django_auth_views
from .views.auth_views import MyLoginView, MyRegisterView
from .views.facilitator.criterias import CreateCriteriaView
from .views.facilitator.scenario import ScenarioView, CreateScenarioView, ScenarioDetailView, ScenarioSubmitView
from .views.facilitator.alternatives import CreateAlternativesView
from .views.expert.index import ExpertPanel,QuestionareView,AlternativesDecisionView
from .views import index as views

new_urls = [
    path("", views.index, name="index"),
    path("accounts/login/", MyLoginView.as_view(), name="login"),
    path("accounts/register/", MyRegisterView.as_view(), name="register"),
    path('logout/', django_auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('scenarios/', ScenarioView.as_view(), name='scenarios'),
    path('scenarios/add', CreateScenarioView.as_view(), name='add_scenario'),
    path('scenarios/view/<pk>', ScenarioDetailView.as_view(), name='scenario-detail'),
    path('scenarios/<pk>/criterias/modify', CreateCriteriaView.as_view(), name='modify-criteria'),
    path('scenarios/<pk>/alternatives/modify', CreateAlternativesView.as_view(), name='modify-alternatives'),
    path('scenarios/<pk>/submit', ScenarioSubmitView.as_view(), name='scenario-submit'),
    path('panel/', ExpertPanel.as_view(), name='expert-panel'),
    path('questionare/alternative/<int:alt1>/<int:alt2>/<str:url>', AlternativesDecisionView.as_view(), name='alternatives-decision'),
    path('questionare/<str:url>', QuestionareView.as_view(), name='questionare'),
]
urlpatterns = new_urls