# Net Admin
IOI Net administration tasks

## Setup

Install docker for starting redis.
```
docker run -d -p 6379:6379 redis
pip install -r requirements.txt # Install required python packages
celery -A remote_tasks.tasks worker --loglevel=info # Run a celery worker
```