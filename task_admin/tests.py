import json
import os.path
from django.test import Client
from django.test import TestCase


class TemplateTest(TestCase):
    fixtures = ["templates.json", "admin.json"]

    def test_fields(self):
        client = Client()
        response = client.get('/api/templates/')
        self.assertEqual(response.status_code, 200)
        templates = response.json()
        required_fields = {'id', 'name', 'author', 'code', 'is_local', 'timeout', 'username'}
        self.assertTrue(len(templates) > 0)
        for template in templates:
            self.assertSetEqual(set(template.keys()), required_fields)

    def test_filtering(self):
        client = Client()
        response = client.get('/api/templates/?is_local=true')
        templates = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(templates) > 0)
        for template in templates:
            self.assertTrue(template['is_local'])

        response = client.get('/api/templates/?is_local=false')
        templates = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(templates) > 0)
        for template in templates:
            self.assertFalse(template['is_local'])

    def test_create(self):
        client = Client()
        data = {'name': 'test', 'author': 1, 'code': 'code', 'is_local': True, 'timeout': 7.0, 'username': ''}
        response = client.post('/api/templates/', data)
        self.assertEqual(response.status_code, 201)
        template = response.json()
        template.pop('id')
        self.assertDictEqual(template, data)

    def test_single_template(self):
        client = Client()
        response = client.get('/api/templates/2/')
        self.assertEqual(response.status_code, 200)
        template = response.json()
        template['is_local'] = not template['is_local']
        put_response = client.put('/api/templates/2/', json.dumps(template), content_type='application/json')
        self.assertDictEqual(put_response.json(), template)
        delete_response = client.delete('/api/templates/2/')
        self.assertEqual(delete_response.status_code, 204)
        self.assertEqual(client.get('/api/templates/2/').status_code, 404)


class TaskTest(TestCase):
    fixtures = ['nodes.json', 'desks.json', 'rooms.json', 'contestants.json', 'admin.json']

    def test_without_task(self):
        task_data = {
            'name': 'touch',
            'code': 'touch /tmp/{contestant.first_name}',
            'is_local': True,
            'timeout': 7.0,
            'username': '',
            'owner': 1,
            'ips': json.dumps(['172.17.0.0', '172.17.0.1'])
        }
        client = Client()
        self.remove_tmp_files()
        self.assertEqual(client.post('/api/tasks/', task_data).status_code, 201)
        taskruns = client.get('/api/taskruns/').json()
        print(taskruns)
        self.assertEqual(int(taskruns['count']), 2)
        self.assertTrue(os.path.isfile('/tmp/TurkishContestant-1'))
        self.assertTrue(os.path.isfile('/tmp/TurkishContestant-2'))
        self.remove_tmp_files()

    def test_timeout(self):
        task_data = {
            'name': 'sleep test',
            'code': 'sleep 2 && touch /tmp/{contestant.first_name}',
            'is_local': True,
            'timeout': 1,
            'username': '',
            'owner': 1,
            'ips': json.dumps(['172.17.0.0', '172.17.0.1'])
        }
        client = Client()
        self.remove_tmp_files()
        self.assertEqual(client.post('/api/tasks/', task_data).status_code, 201)
        taskruns = client.get('/api/taskruns/').json()
        self.assertEqual(int(taskruns['count']), 2)
        for result in taskruns['results']:
            self.assertEqual(result['status'], 'FAILED')
        self.assertFalse(os.path.isfile('/tmp/TurkishContestant-1'))
        self.assertFalse(os.path.isfile('/tmp/TurkishContestant-2'))

    def remove_tmp_files(self):
        if os.path.isfile('/tmp/TurkishContestant-1'):
            os.remove('/tmp/TurkishContestant-1')
        if os.path.isfile('/tmp/TurkishContestant-2'):
            os.remove('/tmp/TurkishContestant-2')

    def test_partial_field(self):
        client = Client()
        task_data = {
            'code': 'touch /tmp/{contestant.first_name}',
            'owner': 1,
            'ips': json.dumps(['192.168.1.0', '192.168.1.1'])
        }
        self.assertEqual(client.post('/api/tasks/', task_data).status_code, 400)

        task_data = {
            'code': 'touch /tmp/{contestant.first_name}',
            'is_local': True,
            'owner': 1,
            'ips': json.dumps(['192.168.1.0', '192.168.1.1'])
        }
        self.assertEqual(client.post('/api/tasks/', task_data).status_code, 400)

        task_data = {
            'owner': 1,
            'ips': json.dumps(['192.168.1.0', '192.168.1.1'])
        }
        self.assertEqual(client.post('/api/tasks/', task_data).status_code, 400)


class CompleteTest(TestCase):
    fixtures = ['admin.json']

    def create_templates(self):
        client = Client()
        template_data = {'name': 'touch', 'author': 1, 'code': 'touch /tmp/{contestant.first_name}', 'is_local': True,
                     'timeout': 7.0, 'username': ''}
        client.post('/api/templates/', template_data)
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
            'first_name': 'amin',
            'country': 'IR',
            'number': 3
        }
        self.assertEqual(client.post('/api/contestants/', contestant_data).status_code, 201)

        contestant_data = {
            'first_name': 'hamed',
            'country': 'IR',
            'number': 2
        }
        self.assertEqual(client.post('/api/contestants/', contestant_data).status_code, 201)

        desk_data = {
            'contestant': 1,
            'active_node': 1,
            'room': 1,
            'number': 1
        }
        self.assertEqual(client.post('/api/desks/', desk_data).status_code, 201)

        desk_data = {
            'contestant': 2,
            'active_node': 2,
            'room': 1,
            'number': 2
        }
        self.assertEqual(client.post('/api/desks/', desk_data).status_code, 201)

        task_data = {
            'name': 'touch',
            'code': template_data['code'],
            'is_local': template_data['is_local'],
            'timeout': template_data['timeout'],
            'username': template_data['username'],
            'owner': 1,
            'ips': json.dumps(['192.168.1.1', '192.168.1.2'])
        }

        self.remove_tmp_files()
        self.assertEqual(client.post('/api/tasks/', task_data).status_code, 201)
        taskruns = client.get('/api/taskruns/').json()
        self.assertEqual(int(taskruns['count']), 2)
        self.assertTrue(os.path.isfile('/tmp/hamed'))
        self.assertTrue(os.path.isfile('/tmp/amin'))
        self.remove_tmp_files()

    def remove_tmp_files(self):
        if os.path.isfile('/tmp/hamed'):
            os.remove('/tmp/hamed')
        if os.path.isfile('/tmp/amin'):
            os.remove('/tmp/amin')

    def test_everything(self):
        self.create_templates()
