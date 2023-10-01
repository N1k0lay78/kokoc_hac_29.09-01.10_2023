from datetime import datetime
from data.activity import Activity
from data.statistics import Statistics
from data.InnerAPI.main_file import raise_error, check_user
from sqlalchemy import and_


def get_list_statistics(user_email):
    user, session = check_user(user_email)
    data = []
    for item in session.query(Statistics).all():
        elem = item.to_dict(only=("start_date", "history", 'all', 'activity_id'))
        data.append(elem)
    session.close()
    return data


def get_statistics(user_email, activity_id):
    user, session = check_user(user_email)
    if type(user) is dict:
        return user

    activity = session.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        return raise_error("Как это вообще возможно? Активность не найдена", session)[0]

    statistics = session.query(Statistics).filter(and_(Statistics.user_id == user.id, Statistics.activity_id == activity_id))

    data = statistics.to_dict(only=("start_date", "history", 'all', 'activity_id'))
    session.close()
    return data


def put_statistics(user_email, activity_id, today_count):
    user, session = check_user(user_email)
    if type(user) is dict:
        return user

    activity = session.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        return raise_error("Как это вообще возможно? Активность не найдена", session)[0]

    statistics = session.query(Statistics).filter(and_(Statistics.user_id == user.id, Statistics.activity_id == activity_id))
    statistics.all += today_count
    statistics.history += f'/{today_count}'
    session.commit()
    session.close()
    return {"success": f"Статистика успешно изменена"}


def create_statistics(user_email, activity_id):
    user, session = check_user(user_email)

    if type(user) is dict:
        return user

    activity = session.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        session.close()
        return {"error": "активность не найдена"}

    new_statistics = Statistics()
    new_statistics.history = ""
    new_statistics.all = 0
    new_statistics.start_date = datetime.now()

    user.add(new_statistics)
    activity_id.add(new_statistics)
    session.commit()
    session.close()

    return {'success': f'Статистика создана'}
