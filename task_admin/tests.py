import json
import os.path

from django.test import Client
from django.test import TestCase


class TaskTest(TestCase):
    fixtures = ["tasks.json", "admin.json"]

    def test_fields(self):
        client = Client()
        response = client.get('/api/tasks/')
        self.assertEqual(response.status_code, 200)
        tasks = response.json()
        required_fields = {'id', 'name', 'author', 'code', 'is_local'}
        self.assertTrue(len(tasks) > 0)
        for task in tasks:
            self.assertSetEqual(set(task.keys()), required_fields)

    def test_filtering(self):
        client = Client()
        response = client.get('/api/tasks/?is_local=true')
        tasks = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(tasks) > 0)
        for task in tasks:
            self.assertTrue(task['is_local'])

        response = client.get('/api/tasks/?is_local=false')
        tasks = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(tasks) > 0)
        for task in tasks:
            self.assertFalse(task['is_local'])

    def test_create(self):
        client = Client()
        data = {'name': 'test', 'author': 1, 'code': 'code', 'is_local': True}
        response = client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, 201)
        task = response.json()
        task.pop('id')
        self.assertDictEqual(task, data)

    def test_single_task(self):
        client = Client()
        response = client.get('/api/tasks/2/')
        self.assertEqual(response.status_code, 200)
        task = response.json()
        task['is_local'] = not task['is_local']
        put_response = client.put('/api/tasks/2/', json.dumps(task), content_type='application/json')
        self.assertDictEqual(put_response.json(), task)
        delete_response = client.delete('/api/tasks/2/')
        self.assertEqual(delete_response.status_code, 204)
        self.assertEqual(client.get('/api/tasks/2/').status_code, 404)


class TaskRunSetTest(TestCase):
    fixtures = ['nodes.json', 'desks.json', 'rooms.json', 'contestants.json', 'admin.json']

    def test_without_task(self):
        taskrunset_data = {
            'code': 'touch /tmp/{contestant.name}',
            'is_local': True,
            'owner': 1,
            'ips': json.dumps(['192.168.1.0', '192.168.1.1'])
        }
        client = Client()
        self.remove_tmp_files()
        self.assertEqual(client.post('/api/taskrunsets/', taskrunset_data).status_code, 201)
        taskruns = client.get('/api/taskruns/').json()
        self.assertEqual(len(taskruns), 2)
        self.assertTrue(os.path.isfile('/tmp/TurkishContestant-1'))
        self.assertTrue(os.path.isfile('/tmp/TurkishContestant-2'))
        self.remove_tmp_files()

    def remove_tmp_files(self):
        if os.path.isfile('/tmp/TurkishContestant-1'):
            os.remove('/tmp/TurkishContestant-1')
        if os.path.isfile('/tmp/TurkishContestant-2'):
            os.remove('/tmp/TurkishContestant-2')

    def test_partial_field(self):
        client = Client()
        taskrunset_data = {
            'code': 'touch /tmp/{contestant.name}',
            'owner': 1,
            'ips': json.dumps(['192.168.1.0', '192.168.1.1'])
        }
        self.assertEqual(client.post('/api/taskrunsets/', taskrunset_data).status_code, 400)

        taskrunset_data = {
            'code': 'touch /tmp/{contestant.name}',
            'is_local': True,
            'task': 1,
            'owner': 1,
            'ips': json.dumps(['192.168.1.0', '192.168.1.1'])
        }
        self.assertEqual(client.post('/api/taskrunsets/', taskrunset_data).status_code, 400)

        taskrunset_data = {
            'owner': 1,
            'ips': json.dumps(['192.168.1.0', '192.168.1.1'])
        }
        self.assertEqual(client.post('/api/taskrunsets/', taskrunset_data).status_code, 400)


class CompleteTest(TestCase):
    fixtures = ['admin.json']

    def create_tasks(self):
        client = Client()
        task_data = {'name': 'touch', 'author': 1, 'code': 'touch /tmp/{contestant.name}', 'is_local': True}
        client.post('/api/tasks/', task_data)
        node_data = {
            'ip': '192.168.1.1',
            'mac_address': 'some_mac',
            'username': 'root',
            'property_id': '3',
            'connected': True
        }
        self.assertEqual(client.post('/api/nodes/', node_data).status_code, 201)

        node_data = {
            'ip': '192.168.1.2',
            'mac_address': 'some_mac2',
            'username': 'root',
            'property_id': '32',
            'connected': True
        }
        self.assertEqual(client.post('/api/nodes/', node_data).status_code, 201)

        room_data = {
            'name': 'floor1',
        }
        self.assertEqual(client.post('/api/rooms/', room_data).status_code, 201)

        contestant_data = {
            'name': 'amin',
            'country': 'IR',
            'number': 3
        }
        self.assertEqual(client.post('/api/contestants/', contestant_data).status_code, 201)

        contestant_data = {
            'name': 'hamed',
            'country': 'IR',
            'number': 2
        }
        self.assertEqual(client.post('/api/contestants/', contestant_data).status_code, 201)

        desk_data = {
            'contestant': 1,
            'active_node': 1,
            'room': 1
        }
        self.assertEqual(client.post('/api/desks/', desk_data).status_code, 201)

        desk_data = {
            'contestant': 2,
            'active_node': 2,
            'room': 1
        }
        self.assertEqual(client.post('/api/desks/', desk_data).status_code, 201)

        taskrunset_data = {
            'task': 1,
            'owner': 1,
            'ips': json.dumps(['192.168.1.1', '192.168.1.2'])
        }

        self.remove_tmp_files()
        self.assertEqual(client.post('/api/taskrunsets/', taskrunset_data).status_code, 201)
        taskruns = client.get('/api/taskruns/').json()
        self.assertEqual(len(taskruns), 2)
        self.assertTrue(os.path.isfile('/tmp/hamed'))
        self.assertTrue(os.path.isfile('/tmp/amin'))
        self.remove_tmp_files()

    def remove_tmp_files(self):
        if os.path.isfile('/tmp/hamed'):
            os.remove('/tmp/hamed')
        if os.path.isfile('/tmp/amin'):
            os.remove('/tmp/amin')

    def test_everything(self):
        self.create_tasks()
