from visualization.models import Contestant, Node, Desk


def sample_exception():
    raise Exception("Can't save sample model")


def get_sample_node():
    node = Node()
    node.save = sample_exception
    node.id = 5
    node.ip = '192.168.100.50'
    node.mac_address = 'e6:67:f4:56:90:fc'
    node.username = 'user1'
    node.property_id = 'Intel@45'
    return node


def get_sample_desk():
    desk = Desk()
    desk.save = sample_exception
    desk.room_id = 2
    desk.id = 23
    return desk


def get_sample_contestant():
    contestant = Contestant()
    contestant.save = sample_exception
    contestant.name = 'Kian'
    contestant.id = 64
    return contestant


def get_all_possible_vars():
    return {
        '{node.ip}': lambda context: context['node'].ip,
        '{node.id}': lambda context: context['node'].id,
        '{node.mac_address}': lambda context: context['node'].mac_address,
        '{node.username}': lambda context: context['node'].username,
        '{node.property_id}': lambda context: context['node'].property_id,
        '{desk.room_id}': lambda context: context['desk'].room_id,
        '{desk.id}': lambda context: context['desk'].id,
        '{contestant.id}': lambda context: context['contestant'].id,
        '{contestant.name}': lambda context: context['contestant'].name,
    }


def render_preview(code):
    context = get_sample_context()
    return render_task(code, context)


def get_sample_context():
    context = {'node': get_sample_node(),
               'contestant': get_sample_contestant(),
               'desk': get_sample_desk(),
               }
    return context


def render_task(code, context):
    """

    :param code: code from a single instance of Task model
    :param context: context to format code, usually with node, desk and contestant
    :return: rendered code of task
    """

    for template, getter in get_all_possible_vars().items():
        code = code.replace(template, str(getter(context)))
    return code
