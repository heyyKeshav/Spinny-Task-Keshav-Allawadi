from .models import Box
from django.db.models import Avg
from datetime import timedelta,datetime
from django.utils import timezone
from project.settings import secrets

def checkValidity(user):
    
        A1 = secrets.get("A1",100)
        V1 = secrets.get("V1",100)
        L1 = secrets.get("L1",100)
        L2 = secrets.get("L2",100)
                         
    
        if Box.objects.all().count() == 0 :
            return True

        average_area = Box.objects.aggregate(average_area=Avg('area'))['average_area']
        if average_area  > A1 :
            return False

        average_volume = Box.objects.aggregate(average_volume=Avg('volume'))['average_volume']
        if average_volume > V1:
            return False

        current_date_time = datetime.now()
        datetime_one_week_ago = current_date_time - timedelta(days=7)

        total_boxes_last_week = Box.objects.filter(createdOn__gt = datetime_one_week_ago).count()
        if total_boxes_last_week > L1 :
            return False
        
        total_boxes_last_week_by_user = Box.objects.filter(createdBy = user,createdOn__gt = datetime_one_week_ago).count()
        if total_boxes_last_week_by_user > L2 :
            return False
        
        return True