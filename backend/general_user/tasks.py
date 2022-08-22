from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .models import GeneralUser, UserStatus


def update_status():
    for user in GeneralUser.objects.all():
        user_status = user.userstatus_set.last()
        level = (datetime.now().date() -
                 user_status.date_created.date()).days // 7

        if 1 < user_status.status < 4 and level:
            new_status = user_status.status-level
            UserStatus.objects.create(
                type=4, user=user, status=new_status if new_status > 0 else 1)


scheduler = BackgroundScheduler()
scheduler.add_job(update_status, 'interval', seconds=24*60*60)
scheduler.start()
