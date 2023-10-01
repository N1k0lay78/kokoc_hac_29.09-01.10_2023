from data.company import Company
from data.statistics import Statistics
from data.target import Target
from data.InnerAPI.main_file import raise_error, check_params, check_user, check_company
from data import db_session


def find_target_by_id(id, session):
    target = session.query(Target).get(id)
    if not target:
        return raise_error(f"Цель не найдена", session)
    return target, session


def get_target(target_id):
    session = db_session.create_session()
    target, session = find_target_by_id(target_id, session)
    if type(target) is dict:
        session.close()
        return target
    data = target.to_dict(only=("id", "name", 'description', 'required_amount', 'collected_amount', 'status', 'company_id'))
    session.close()
    return data


def get_target_by_email(email):
    session = db_session.create_session()
    target = session.query(Target).filter(Target.email == email).first()
    if not target:
        session.close()
        return {"message": "Цель не найдена"}
    data = target.to_dict(only=("id", "name", 'description', 'required_amount', 'collected_amount', 'status', 'company_id'))
    session.close()
    return data


def get_list_target():
    session = db_session.create_session()
    data = []
    for item in session.query(Target).all():
        elem = item.to_dict(only=("id", "name", 'description', 'required_amount', 'collected_amount', 'status', 'company_id'))
        data.append(elem)
    session.close()
    return data


def put_target(company_email, target_id, args):
    company, session = check_company(company_email)
    if type(company) is dict:
        return company

    target, session = find_target_by_id(target_id, session)
    target_dict = target.to_dict(only=("name", 'required_amount'))
    keys = list(filter(lambda key: args[key] is not None and key in target_dict and args[key] != target_dict[key],
                       list(args.keys())))
    for key in keys:
        if key == 'name':
            target.name = args['name']
        if key == 'required_amount':
            if target.collected_amount >= args["required_amount"]:
                target.status = True
                target.collected_amount = args["required_amount"]
            elif target.status:
                target.status = False
            target.required_amount = args['required_amount']
    if len(keys) == 0:
        return raise_error("Пустой запрос", session)[0]
    session.commit()
    session.close()
    return {"success": f"Успешно изменено"}


def delete_target(company_email, target_id):
    company, session = check_company(company_email)
    if type(company) is dict:
        return company
    target, session = find_target_by_id(target_id, session)
    if type(target) is dict:
        return target
    name = target.name
    session.delete(target)
    session.commit()
    session.close()
    return {"success": f"Цель {name} удалена"}


def create_target(company_email, args):
    company, session = check_company(company_email, args, ["name", 'description', 'required_amount'])
    if type(company) is dict:
        return company

    new_target = Target()
    new_target.name = args["name"]
    new_target.description = args["description"]
    new_target.required_amount = args['required_amount']
    new_target.collected_amount = 0
    new_target.status = False
    new_target.company_id = company.id

    session.add(new_target)
    session.commit()
    id = new_target.id
    session.close()

    return {'id': id, 'success': f'Новая цель {args["name"]} создана'}
