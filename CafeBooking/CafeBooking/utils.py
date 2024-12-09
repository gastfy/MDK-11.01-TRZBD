from .models import Log


def log(action: str):
    new_log = Log()
    new_log.action = action
    new_log.save()
