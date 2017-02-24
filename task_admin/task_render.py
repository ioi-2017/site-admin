from task_admin.models import Task, TaskRunSet, TaskRun
from task_admin.tasks import execute_task
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
    context = get_sample_context()
    return {
        '{node.ip}': context['node'].ip,
        '{node.id}': context['node'].id,
        '{node.mac_address}': context['node'].mac_address,
        '{node.username}': context['node'].username,
        '{node.property_id}': context['node'].property_id,
        '{desk.room_id}': context['desk'].room_id,
        '{desk.id}': context['desk'].id,
        '{contestant.id}': context['contestant'].id,
        '{contestant.name}': context['contestant'].name,
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
    return code.format(**context)


def make_taskrunset(task, desks):
    run_set = TaskRunSet()
    run_set.task = task
    run_set.save()
    for desk in desks:
        task_run = TaskRun()
        task_run.run_set = run_set
        task_run.is_local = task.is_local
        task_run.node = desk.active_node
        task_run.desk = desk
        task_run.contestant = desk.contestant
        task_run.rendered_code = render_task(task.code, context={'node': desk.active_node,
                                                                 'contestant': desk.contestant,
                                                                 'desk': desk,
                                                                 })
        task_run.celery_task = execute_task.delay(**task_run.get_execution_dict()).id
        task_run.save()
