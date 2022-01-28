from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from .models import OCRCameraAlert, SpaceAlert, Space, Visitor, SpaceEvent
from django.db.models import Count
from django.db.models.functions import TruncDay
from datetime import timedelta
from django.utils import timezone


# Create your views here.
class OCRCameraAlertListView(ListView):
    template_name = "ocralert_list.html"
    model = OCRCameraAlert
    paginate_by = 10 


class SpaceAlertListView(ListView):
    template_name = "spacealert_list.html"
    model = SpaceAlert
    paginate_by = 10 

    
class OccupancyReportView(TemplateView):
    template_name = 'occupancy_report.html'

    def get_context_data(self, **kwargs):
        context = super(OccupancyReportView, self).get_context_data(**kwargs)

        space_total = Space.objects.all().count()
        space_total_occupancy = Space.objects.filter(status=2).count()

        current_visitors_count = Visitor.objects.filter(status=1).count()
        special_space_occupancy = Space.objects.filter(status=2, type=2).count()
        special_space_count = Space.objects.filter(type=2).count()

        some_day_last_week = timezone.now().date() - timedelta(days=7) 
        
        visitor_7_days_count = Visitor.objects.filter(
            enter_date__gte=some_day_last_week,
        ).values('enter_date__date').annotate(count=Count('id')).values('enter_date__date', 'count').order_by('enter_date__date')
      

        context['space_total'] = space_total
        context['space_total_occupancy'] = space_total_occupancy
        context['space_total_availability'] = space_total - space_total_occupancy
        context['current_visitors_count'] = current_visitors_count
        context['special_space_occupancy'] = special_space_occupancy
        context['special_space_count'] = special_space_count
        context['visitor_7_days_count'] = visitor_7_days_count
        
        return context


class SpaceMostUsedReportView(ListView):
    template_name = "most_used_spaces_report.html"
    model = SpaceEvent
    paginate_by = 10 

    def get_queryset(self):        
        queryset = SpaceEvent.objects.filter(type=2).values('space__code', 'space__sector').annotate(count=Count('space')).order_by('-count')
        
        return queryset