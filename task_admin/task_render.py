def get_all_possible_vars():
    return {
        '{node.ip}': lambda node: node.ip,
        '{node.id}': lambda node: node.id,
        '{node.mac_address}': lambda node: node.mac_address,
        '{node.username}': lambda node: node.username,
        '{node.property_id}': lambda node: node.property_id,
        '{desk.zone_id}': lambda node: node.desk.zone_id,
        '{desk.id}': lambda node: node.desk.identifier,
        '{contestant.id}': lambda node: node.desk.contestant.identifier,
        '{contestant.name}': lambda node: node.desk.contestant.name,
        '{contestant.first_name}': lambda node: node.desk.contestant.first_name,
        '{contestant.last_name}': lambda node: node.desk.contestant.last_name,
        '{contestant.email}': lambda node: node.desk.contestant.email,
        '{contestant.gender}': lambda node: node.desk.contestant.gender,
    }


def get_all_possible_vars_sample():
    return {
        '{node.ip}': '192.168.100.50',
        '{node.id}': 5,
        '{node.mac_address}': 'e6:67:f4:56:90:fc',
        '{node.username}': 'user1',
        '{node.property_id}': 'Intel@45',
        '{desk.zone_id}': 2,
        '{desk.id}': 'F14',
        '{contestant.id}': 'IRN1',
        '{contestant.name}': 'Kian Mirjalali',
        '{contestant.first_name}': 'Kian',
        '{contestant.last_name}': 'Mirjalali',
        '{contestant.email}': 'mirjalali@gmail.com',
        '{contestant.gender}': 'M',
    }


def render_task(code, node):
    """

    :param code: code from a single instance of Task model
    :param node: node to format code with its context, usually connected to a desk and contestant
    :return: rendered code of task
    """

    for template, getter in get_all_possible_vars().items():
        if template in code:
            try:
                code = code.replace(template, str(getter(node)))
            except:
                raise Exception("Can't use %s since it is not filled for all nodes" % template)
    return code
