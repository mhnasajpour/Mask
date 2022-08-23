from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .models import GeneralUser, UserStatus
from config.settings import WHITEPLACE, REDPLACE
from public_place.models import BusinessOwner, PlaceStatus


def update_status():
    for user in [obj for obj in GeneralUser.objects.all() if 1 < obj.status < 4]:
        user_status = user.userstatus_set.last()
        level = (datetime.now().date() -
                 user_status.date_created.date()).days // 7
        if level:
            new_status = user_status.status-level
            UserStatus.objects.create(
                type=4, user=user, status=new_status if new_status > 0 else 1)

    for place in [obj for obj in BusinessOwner.objects.all() if obj.status == REDPLACE]:
        if (datetime.now().date() - place.placestatus_set.last().date_created.date()).days >= 14:
            PlaceStatus.objects.create(type=3, place=place, status=WHITEPLACE)


scheduler = BackgroundScheduler()
scheduler.add_job(update_status, 'interval', seconds=24*60*60)
scheduler.start()
