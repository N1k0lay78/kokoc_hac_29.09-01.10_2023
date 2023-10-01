from data.activity import Activity
from data.statistics import Statistics
from data.InnerAPI.main_file import raise_error, check_params, check_admin
from data import db_session


def find_by_id(id, session):
    activity = session.query(Activity).get(id)
    if not activity:
        return raise_error(f"Активность не найдена", session)
    return activity, session


def get_activity(activity_id):
    session = db_session.create_session()
    activity, session = find_by_id(activity_id, session)
    if type(activity) is dict:
        session.close()
        return activity
    data = activity.to_dict(only=("id", "name", 'coast', 'conventional_unit', 'type', 'description', 'image',
                                  'base_count'))
    session.close()
    return data


def get_activity_by_name(name):
    session = db_session.create_session()
    activity = session.query(Activity).filter(Activity.name == name).first()
    if not activity:
        session.close()
        return {"message": "Активность не найдена"}
    data = activity.to_dict(only=("id", "name", 'coast', 'conventional_unit', 'type', 'description', 'image',
                                  'base_count'))
    session.close()
    return data


def get_list_activity():
    session = db_session.create_session()
    data = []
    for item in session.query(Activity).all():
        elem = item.to_dict(only=("id", "name", 'coast', 'conventional_unit', 'type', 'description', 'image',
                                  'base_count'))
        data.append(elem)
    session.close()
    return data


def put_activity(admin_email, activity_id, args):
    admin, session = check_admin(admin_email)
    if type(admin) is dict:
        return admin

    activity = find_by_id(activity_id, session)
    if type(activity) is dict:
        return activity

    activity_dict = activity.to_dict(only=("name", 'coast', 'conventional_unit', 'type', 'description', 'image',
                                           'base_count'))
    keys = list(filter(lambda key: args[key] is not None and key in activity_dict and args[key] != activity_dict[key],
                       list(args.keys())))
    for key in keys:
        if key == 'name':
            if session.query(Activity).filter(Activity.name == args["name"]).first():
                return raise_error("Это название уже занято", session)[0]
            activity.name = args['name']
        if key == 'coast':
            activity.coast = args['coast']
        if key == 'conventional_unit':
            activity.conventional_unit = args['conventional_unit']
        if key == 'type':
            activity.type = args['type']
        if key == 'description':
            activity.description = args['description']
        if key == 'image':
            activity.image = args['image']
        if key == 'base_count':
            activity.base_count = args['base_count']
    if len(keys) == 0:
        return raise_error("Пустой запрос", session)[0]
    session.commit()
    session.close()
    return {"success": f"Активность успешно изменена"}


def delete_activity(admin_email, activity_id):
    admin, session = check_params(admin_email)
    if type(admin) is dict:
        return admin
    activity, session = find_by_id(activity_id, session)
    if type(activity) is dict:
        return activity
    for statistics in session.query(Statistics).filter(Statistics.activity_id == activity_id).all():
        session.delete(statistics)
    name = activity.name
    session.delete(activity)
    session.commit()
    session.close()
    return {"success": f"Активность {name} удалена"}


def create_activity(admin_email, args):
    admin, session = check_params(admin_email, args, ["name", 'coast', 'conventional_unit', 'type', 'description', 'base_count'])

    if type(admin) is dict:
        return admin

    new_activity = Activity()
    new_activity.name = args["name"]
    new_activity.coast = args["coast"]
    new_activity.conventional_unit = args['conventional_unit']
    new_activity.type = args['type']
    new_activity.description = args['description']
    new_activity.base_count = args['base_count']
    if 'image' not in args:
        new_activity.image = "./static/img/base_activity.png"
    else:
        new_activity.image = args["image"]
    admin.add(new_activity)
    session.commit()
    id = new_activity.id
    session.close()

    return {'id': id, 'success': f'Новая активность {args["name"]} создана'}
