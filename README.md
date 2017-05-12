# Net Admin
IOI Net administration tasks

## Setup

Install docker for starting redis and postgres:
```
docker run -d -p 6379:6379 --name netadmin-redis redis
docker run -d -p 5432:5432 --name netadmin-postgres -e POSTGRES_PASSWORD=mysecretpassword postgres
```

Install npm and bower for downloading js dependencies:
```
bower install
```

Net Admin has only been tested with python3 and **will not work with python2**.   
Install the required python modules:
```
pip install -r requirements.txt # Install required python packages
```

Run the celery workers:
```
celery -A task_admin.tasks worker --concurrency=2 -Q local_queue --loglevel=info # Run a celery worker for local tasks
celery -A task_admin.tasks worker --concurrency=10 -Q remote_queue --loglevel=info # Run a celery worker for remote tasks
./start-workers.sh # To run both workers
```

Import fixtures if necessary:
```
./manage.py loaddata task_admin/fixtures/admin.json
./manage.py loaddata task_admin/fixtures/tasks.json
./manage.py loaddata visualization/fixtures/rooms.json
./manage.py loaddata visualization/fixtures/contestants.json
./manage.py loaddata visualization/fixtures/nodes.json
./manage.py loaddata visualization/fixtures/desks.json
```


## Concepts

### `Task`
  A single command that can be used to create TaskRunSets, for example "locking the keyboards".

  Each task has a piece of code for execution, tasks can be local or remote. In remote tasks, the 
  code is executed directly on the remote machine through ssh. In local tasks, the code is executed on the server machine.

### `TaskRun`
 Execution of a single command on a single node, for example "locking the keyboard on contestant X"

### `TaskRunSet`
 Execution of a single command on a set of nodes, for example "locking the keyboards of all contestants"

### `Desk`
 A wooden desk! usually with a node attached to it and with locations for visualization purposes.

### `Contestant`
 Single person participating in the contest, assigned to a desk and node, having information like name and country.

### `Node`
 A node is a single pc with ip address.


## Development

Right now we are using celery for scheduling, redis for the broker backend and postgres for result backend.
