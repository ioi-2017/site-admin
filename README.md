# Net Admin
IOI Net administration tasks

## Setup

Install docker for starting redis.
```
docker run -d -p 6379:6379 redis
pip install -r requirements.txt # Install required python packages
celery -A remote_tasks.tasks worker --loglevel=info # Run a celery worker
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



## Development

Right now we are using celery for scheduling, redis for the broker backend and postgres for result backend.