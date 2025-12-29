from django.urls import path
from . import views

app_name = 'ai'

urlpatterns = [
    path('at-risk-students/', views.at_risk_students, name='at_risk_students'),
    path('bias-alerts/', views.bias_alerts, name='bias_alerts'),
    path('student-insights/<str:student_id>/', views.student_insights, name='student_insights'),
    path('workload-forecast/', views.workload_forecast, name='workload_forecast'),
    path('assignment-grade-suggest/', views.assignment_grade_suggest, name='assignment_grade_suggest'),
]

