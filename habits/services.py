from datetime import datetime, timedelta


def is_time_to_send_reminder(habit):
    """Вычисление разницы между настоящим временем и временем, когда задача должна начаться. Если разница менее 5 минут, вернется True."""
    tolerance_minutes = 5

    now = datetime.now()

    start_time_moscow = datetime.combine(now.date(), habit.start_time)

    delta = abs(now - start_time_moscow)

    return delta <= timedelta(minutes=tolerance_minutes)
