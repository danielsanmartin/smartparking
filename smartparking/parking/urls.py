from django.urls import path
from .views import OCRCameraAlertListView, SpaceAlertListView, OccupancyReportView, SpaceMostUsedReportView

app_name = 'parking'

urlpatterns = [
    path('', OCRCameraAlertListView.as_view(), name='index'),
    path('orcalert/list/', OCRCameraAlertListView.as_view(), name='ocralert_list'),
    path('spacealert/list/', SpaceAlertListView.as_view(), name='spacealert_list'),
    path('report/occupancy/', OccupancyReportView.as_view(), name='occupancy_report'),
    path('report/spacemostused/', SpaceMostUsedReportView.as_view(), name='space_most_used_report'),    
]
