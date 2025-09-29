from django.urls import path
from . import views

urlpatterns = [
    path('options/', views.OptionsList.as_view(), name='options'),
    path('labresults/', views.LabResultList.as_view(), name='labresults'),
]
