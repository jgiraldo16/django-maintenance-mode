import maintenance.settings as maintenance_settings
from datetime import datetime, timedelta
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import MaintenancePeriod

class MaintenanceModeMiddleware(object):
    def process_request(self, request):
        now = datetime.now()
        
        # Checking to see if there are any current maintenance periods.

        maintenance = MaintenancePeriod.objects.filter(start_date__lt=now, end_date__gt=now)
        if maintenance and request.META['REMOTE_ADDR'] not in maintenance_settings.SAFE_IP:
            if maintenance[0].template:
                return render_to_response(maintenance[0].template, context_instance=RequestContext(request))
            else:
                return render_to_response(maintenance_settings.TEMPLATE, context_instance=RequestContext(request))

        return None

