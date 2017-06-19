def get_all_possible_vars():
    return {
        '{node.ip}': lambda node: node.ip,
        '{node.id}': lambda node: node.id,
        '{node.mac_address}': lambda node: node.mac_address,
        '{node.username}': lambda node: node.username,
        '{node.property_id}': lambda node: node.property_id,
        '{desk.room_id}': lambda node: node.desk.room_id,
        '{desk.id}': lambda node: node.desk.id,
        '{contestant.id}': lambda node: node.desk.contestant.id,
        '{contestant.name}': lambda node: node.desk.contestant.name,
    }


def get_all_possible_vars_sample():
    return {
        '{node.ip}': '192.168.100.50',
        '{node.id}': 5,
        '{node.mac_address}': 'e6:67:f4:56:90:fc',
        '{node.username}': 'user1',
        '{node.property_id}': 'Intel@45',
        '{desk.room_id}': 2,
        '{desk.id}': 23,
        '{contestant.id}': 64,
        '{contestant.name}': 'Kian',
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
