# API Index:
#### [Task](#task-api)
#### [TaskRun](#taskrun-api)
#### [TaskRunSet](#taskrunset-api)
#### [Node](#node-api)
#### [Desk](#desk-api)
#### [Room](#room-api)
#### [Contestant](#contestant-api)

**Task API**
----

***Task List***

   Returns a list of task based on filtering criteria

* **URL**

      /api/tasks/

* **Method:**

      `GET`

*  **URL Params**

     You can filter the returning list using optional arguments in get request.

     **Optional:**

     `id=[integer]`
     `name=[string]`
     `author=[integer]`
     `is_local=[boolean]`

* **Success Response:**

     On success a list of tasks with their attributes is returned

      * **Code:** 200 <br />
        **Content:**
        ```
        [
        {
            "id": 1,
            "name": "scp",
            "author": 1,
            "code": "scp /home/ioi/tasks/{node.id} {node.username}@{node.ip}:tasks/",
            "is_local": true
        },
        {
            "id": 2,
            "name": "ls2",
            "author": 1,
            "code": "ls -lah",
            "is_local": false
        }
        ]
        ```

* **Sample Call:**
       ```
       curl 'http://localhost:8000/api/tasks/?name=test&author=1&is_local=true'
       ```

***Task Creation***

   Create a new task

* **URL**

    /api/tasks/

* **Method:**

    `POST`

* **Data Params**

     Values for the new task

     **Required:**

     `name=[string]`
     `author=[integer]`
     `code=[string]`
     `is_local=[boolean]`

* **Success Response:**

      Returns the task created

      * **Code:** 201 Created <br />
        **Content:**
        ```
        {
        "id": 3,
        "name": "test",
        "author": 1,
        "code": "test",
        "is_local": true
        }
        ```

* **Sample Call:**
       ```
       curl -X POST -F "name=test" -F "author=1" -F "code=test" "http://localhost:8000/api/tasks/"
       ```

***Single Task Modification/Deletion***

   Fetch, update or delete task

* **URL**

    /api/tasks/<?task_id>/

* **Method:**

    `GET` | `PUT` | `PATCH` | `DELETE`

* **Data Params**

     Params used for updating the task

     **Required for `PUT` and Optional for `PATCH`:**

     `name=[string]`
     `author=[integer]`
     `code=[string]`
     `is_local=[boolean]`

* **Success Response:**

      For `GET`, `PATCH`, and `PUT` returns the task:

      * **Code:** 200 OK <br />
        **Content:**
        ```
        {
        "id": 3,
        "name": "test",
        "author": 1,
        "code": "test",
        "is_local": true
        }
        ```

      OR

      If all parameters are not given in `PUT`

     * **Code:** 400 Bad Request<br />

      OR

      * **Code:** 404 Not Found <br />

      For delete returns nothing:

      * **Code:** 204 No Content <br />

* **Sample Call:**
       ```
       curl -X PATCH "code=updated_test" "http://localhost:8000/api/tasks/3/"
       curl -X PUT -F "name=test" -F "author=1" -F "code=updated_test" "http://localhost:8000/api/tasks/3/"
       curl "http://localhost:8000/api/tasks/3/"
       curl -X DELETE "http://localhost:8000/api/tasks/3/"
       ```

**TaskRun API**
----

***TaskRun List***

   Returns a list of task runs based on filtering criteria

* **URL**

      /api/taskruns/

* **Method:**

      `GET`

*  **URL Params**

     You can filter the returning list using optional arguments in get request.

     **Optional:**

     `desk=[integer]`
     `contestant=[string]`
     `node=[integer]`

* **Success Response:**

     On success a list of task runs with their attributes is returned

      * **Code:** 200 <br />
        **Content:**
        ```
        [
            {
                "id": 7,
                "celery_task": "6d007e1f-0841-4b55-8501-80a06e503023",
                "is_local": true,
                "run_set": 11,
                "created_at": "2017-03-18T17:17:29.117358Z",
                "started_at": "2017-03-18T20:47:29.116026+03:30",
                "finished_at": "2017-03-18T20:47:29.154596+03:30",
                "rendered_code": "test",
                "desk": 1,
                "contestant": 1,
                "node": 1
            },
            {
                "id": 9,
                "celery_task": "2c8250dd-31c4-48c8-ac97-aeffb2fc404a",
                "is_local": true,
                "run_set": 12,
                "created_at": "2017-03-18T17:20:02.505968Z",
                "started_at": "2017-03-18T20:50:02.503324+03:30",
                "finished_at": "2017-03-18T20:50:02.531218+03:30",
                "rendered_code": "test",
                "desk": 1,
                "contestant": 1,
                "node": 1
            }
        ]
        ```

* **Sample Call:**
       ```
       curl 'http://localhost:8000/api/taskruns/?node=1'
       ```

***Single TaskRun fetch***

   Fetch a single taskrun

* **URL**

    /api/taskruns/<?taskrun_id>/

* **Method:**

    `GET`

* **Success Response:**

      Returns the task run:

      * **Code:** 200 OK <br />
        **Content:**
        ```
        {
            "id": 6,
            "celery_task": "4983bb35-941d-43c5-ac12-227bf01a1076",
            "is_local": true,
            "run_set": 11,
            "created_at": "2017-03-18T17:17:29.109260Z",
            "started_at": "2017-03-18T20:47:29.071587+03:30",
            "finished_at": "2017-03-18T20:47:29.144748+03:30",
            "rendered_code": "test",
            "desk": 3,
            "contestant": 2,
            "node": 3
        }
        ```

* **Sample Call:**
       ```
       curl "http://localhost:8000/api/taskruns/6/"
       ```

**TaskRunSet API**
----

***TaskRunSet List***

   Returns a list of taskrun sets based on filtering criteria augmented with pagination stuff

* **URL**

      /api/taskrunsets/

* **Method:**

      `GET`

*  **URL Params**

     You can filter the returning list using optional arguments in get request.

     **Optional:**

     `task=[integer]`

* **Success Response:**

     On success a list of task runs with their attributes is returned

      * **Code:** 200 <br />
        **Content:**

        ```
        {
            "count": 12,
            "next": "http://localhost:8000/api/taskrunsets/?page=2",
            "previous": null,
            "results": [
                {
                    "id": 2,
                    "task": 1,
                    "task_data": {
                        "id": 1,
                        "name": "new_scp",
                        "author": 1,
                        "code": "scp /home/ioi/tasks/{node.id} {node.username}@{node.ip}:tasks/",
                        "is_local": true
                    },
                    "owner": 1,
                    "owner_data": "admin",
                    "created_at": "2017-03-08T16:37:57.075553Z",
                    "taskruns": [
                        "[test] on 192.168.200.20",
                        "[test] on 192.168.200.10"
                    ]
                },
                .
                . //More items here
                .
                {
                    "id": 12,
                    "task": 4,
                    "task_data": {
                        "id": 4,
                        "name": "test",
                        "author": 1,
                        "code": "test",
                        "is_local": true
                    },
                    "owner": 1,
                    "owner_data": "admin",
                    "created_at": "2017-03-18T17:20:02.377168Z",
                    "taskruns": [
                        "[test] on 192.168.200.20",
                        "[test] on 192.168.200.10"
                    ]
                }
            ],
            "pagination": {
                "page_links": [
                    [
                        "http://localhost:8000/api/taskrunsets/",
                        1,
                        true,
                        false
                    ],
                    [
                        "http://localhost:8000/api/taskrunsets/?page=2",
                        2,
                        false,
                        false
                    ]
                ],
                "next_url": "http://localhost:8000/api/taskrunsets/?page=2",
                "previous_url": null
            }
        }

        ```

* **Sample Call:**
       ```
       curl 'http://localhost:8000/api/taskrunsets/?task=5'
       ```

***TaskRunSet Creation***

   Create a new taskrun set

* **URL**

    /api/taskrunsets/

* **Method:**

    `POST`

* **Data Params**

     Values for the new task

     **Required:**

     `task=[integer]`
     `owner=[integer]`
     `ips=[json]`

* **Success Response:**

      Returns the task created

      * **Code:** 201 Created <br />
        **Content:**
        ```
        {
            "id": 13,
            "task": 5,
            "task_data": {
                "id": 5,
                "name": "test",
                "author": 1,
                "code": "test",
                "is_local": true
            },
            "owner": 1,
            "owner_data": "admin",
            "created_at": "2017-03-18T17:24:02.413501Z",
            "taskruns": [
                "[test] on 192.168.200.20"
            ]
        }
        ```

* **Sample Call:**
       ```
       curl -X POST -F "ips=[\"192.168.200.20\"]" -F "owner=1" -F "task=5" "http://localhost:8000/api/taskrunsets/"
       ```


***Single TaskRunSet fetch***

   Fetch a single taskrun set

* **URL**

    /api/taskrunsets/<?taskrunset_id>/

* **Method:**

    `GET`

* **Success Response:**

      Returns the task run:

      * **Code:** 200 OK <br />
        **Content:**
        ```
        {
            "id": 13,
            "task": 5,
            "task_data": {
                "id": 5,
                "name": "test",
                "author": 1,
                "code": "test",
                "is_local": true
            },
            "owner": 1,
            "owner_data": "admin",
            "created_at": "2017-03-18T17:24:02.413501Z",
            "taskruns": [
                "[test] on 192.168.200.20"
            ]
        }
        ```

* **Sample Call:**
       ```
       curl "http://localhost:8000/api/taskrunsets/13/"
       ```


**Node API**
----

***Node List***

   Returns a list of node based on filtering criteria

* **URL**

      /api/nodes/

* **Method:**

      `GET`

*  **URL Params**

     You can filter the returning list using optional arguments in get request.

     **Optional:**

     `id=[integer]`
     `ip=[string]`
     `mac_address=[string]`
     `username=[string]`
     `property_id=[string]`
     `connected=[boolean]`

* **Success Response:**

     On success a list of tasks with their attributes is returned

      * **Code:** 200 <br />
        **Content:**
        ```
        [
            {
                "id": 1,
                "ip": "192.168.200.10",
                "mac_address": "01:23:45:67:89:AB",
                "username": "admin",
                "property_id": "2",
                "connected": true
            },
            {
                "id": 2,
                "ip": "192.168.200.11",
                "mac_address": "5e:7e:13:76:88:5a",
                "username": "admin",
                "property_id": "3",
                "connected": false
            }
        ]
        ```

* **Sample Call:**
       ```
       curl 'http://localhost:8000/api/nodes/?connected=false'
       ```

***Node Creation***

   Create a new node

* **URL**

    /api/nodes/

* **Method:**

    `POST`

* **Data Params**

     Values for the new task

     **Required:**

     `ip=[string]`
     `mac_address=[string]`
     `username=[string]`
     `property_id=[string]`
     `connected=[boolean]`

* **Success Response:**

      Returns the task created

      * **Code:** 201 Created <br />
        **Content:**
        ```
        {
          "id": 3,
          "ip": "192.168.200.20",
          "mac_address": "42:42:42:42:42:42",
          "username": "admin",
          "property_id": "4",
          "connected": true
        }
        ```

* **Sample Call:**
       ```
       curl -X POST -F "ip=192.168.200.20" -F "mac_address=42:42:42:42:42:42" -F "username=admin" -F "property_id=4" -F "connected=true" "http://localhost:8000/api/nodes/"
       ```

***Single Node Modification/Deletion***

   Fetch, update or delete task

* **URL**

    /api/nodes/<?node_id>/

* **Method:**

    `GET` | `PUT` | `PATCH` | `DELETE`

* **Data Params**

     Params used for updating the node

     **Required for `PUT` and Optional for `PATCH`:**

     `ip=[string]`
     `mac_address=[string]`
     `username=[string]`
     `property_id=[string]`
     `connected=[boolean]`

* **Success Response:**

      For `GET`, `PATCH`, and `PUT` returns the task:

      * **Code:** 200 OK <br />
        **Content:**
        ```
        {
          "id": 3,
          "ip": "192.168.200.20",
          "mac_address": "42:42:42:42:42:42",
          "username": "admin",
          "property_id": "4",
          "connected": true
        }
        ```

      OR

      If all parameters are not given in `PUT`

     * **Code:** 400 Bad Request<br />

      OR

      * **Code:** 404 Not Found <br />

      For delete returns nothing:

      * **Code:** 204 No Content <br />

* **Sample Call:**
       ```
       curl -X PUT -F "ip=192.168.200.20" -F "mac_address=43:42:42:42:42:42" -F "username=admin" -F  "property_id=4" -F "connected=true" "http://localhost:8000/api/nodes/3/"
       ```
       ```
       curl -X PATCH "username=patched_admin" -F "property_id=4" -F "connected=true" "http://localhost:8000/api/nodes/3/"
       ```
       ```
       curl "http://localhost:8000/api/nodes/3/"
       ```
       ```
       curl -X DELETE "http://localhost:8000/api/nodes/3/"
       ```

**Room API**
----

***Room List***

   Returns the list of all rooms created

* **URL**

      /api/rooms/

* **Method:**

      `GET`

* **Success Response:**

     On success a list of rooms with their attributes is returned

      * **Code:** 200 <br />
        **Content:**
        ```
        [
            {
                "id": 1,
                "name": "floor1"
            },
            {
                "id": 2,
                "name": "floor2"
            }
        ]
        ```

* **Sample Call:**
       ```
       curl 'http://localhost:8000/api/rooms/
       ```

***Room Creation***

   Create a new room

* **URL**

    /api/rooms/

* **Method:**

    `POST`

* **Data Params**

     Values for the new task

     **Required:**

     `name=[string]`

* **Success Response:**

      Returns the task created

      * **Code:** 201 Created <br />
        **Content:**
        ```
        {
            "id": 3,
            "name": "floor3"
        }
        ```

* **Sample Call:**
       ```
       curl -X POST -F "name=floor3" "http://localhost:8000/api/rooms/"
       ```

***Single Room Modification/Deletion***

   Fetch, update or delete room

* **URL**

    /api/rooms/<?room_id>/

* **Method:**

    `GET` | `PUT` | `PATCH` | `DELETE`

* **Data Params**

     Params used for updating the room

     **Required for `PUT` and Optional for `PATCH`:**

     `name=[string]`

* **Success Response:**

      For `GET`, `PATCH`, and `PUT` returns the task:

      * **Code:** 200 OK <br />
        **Content:**
        ```
        {
            "id": 3,
            "name": "floor3"
        }
        ```

      OR

      If all parameters are not given in `PUT`

     * **Code:** 400 Bad Request<br />

      OR

      * **Code:** 404 Not Found <br />

      For delete returns nothing:

      * **Code:** 204 No Content <br />

* **Sample Call:**
       ```
       curl -X PUT -F "name=floor4" "http://localhost:8000/api/rooms/3/"
       ```
       ```
       curl -X PATCH -F "name=floor4" "http://localhost:8000/api/rooms/3/"
       ```
       ```
       curl "http://localhost:8000/api/rooms/3/"
       ```
       ```
       curl -X DELETE "http://localhost:8000/api/rooms/3/"
       ```

**Contestant API**
----

***Contestant List***

   Returns a list of contestants based on filtering criteria

* **URL**

      /api/contestants/

* **Method:**

      `GET`

*  **URL Params**

     You can filter the returning list using optional arguments in get request.

     **Optional:**

     `country=[string]`
     `number=[integer]`

* **Success Response:**

     On success a list of contestants with their attributes is returned

      * **Code:** 200 <br />
        **Content:**
        ```
        [
            {
                "id": 1,
                "name": "Amin",
                "country": "IR",
                "number": 4
            },
            {
                "id": 2,
                "name": "Hamed",
                "country": "US",
                "number": 1
            }
        ]
        ```

* **Sample Call:**
       ```
       curl 'http://localhost:8000/api/contestants/
       ```

***Contestant Creation***

   Create a new contestant

* **URL**

    /api/contestants/

* **Method:**

    `POST`

* **Data Params**

     Values for the new contestant

     **Required:**

     `name=[string]`
     `country=[string]`: Two letter code of the country (e.g IR)
     `number=[integer]`

* **Success Response:**

      Returns the contestant created

      * **Code:** 201 Created <br />
        **Content:**
        ```
        {
            "id": 1,
            "name": "Amin",
            "country": "IR",
            "number": 4
        }
        ```

* **Sample Call:**
       ```
       curl -X POST -F "name=Amin" -F "country=IR" -F "number=4" "http://localhost:8000/api/contestants/"
       ```

***Single Contestant Modification/Deletion***

   Fetch, update or delete contestant

* **URL**

    /api/contestants/<?contestant_id>/

* **Method:**

    `GET` | `PUT` | `PATCH` | `DELETE`

* **Data Params**

     Params used for updating the contestant

     **Required for `PUT` and Optional for `PATCH`:**

     `name=[string]`
     `country=[string]`
     `number=[integer]`

* **Success Response:**

      For `GET`, `PATCH`, and `PUT` returns the task:

      * **Code:** 200 OK <br />
        **Content:**
        ```
        {
            "id": 1,
            "name": "Amin",
            "country": "IR",
            "number": 4
        }
        ```

      OR

      If all parameters are not given in `PUT`

     * **Code:** 400 Bad Request<br />

      OR

      * **Code:** 404 Not Found <br />

      For delete returns nothing:

      * **Code:** 204 No Content <br />

* **Sample Call:**
       ```
       curl -X PUT -F "name=Amin2" -F "country=IR" -F "number=4" "http://localhost:8000/api/contestants/1/"
       ```
       ```
       curl -X PATCH -F "name=Amin2" "http://localhost:8000/api/contestants/1/"
       ```
       ```
       curl "http://localhost:8000/api/contestants/1/"
       ```
       ```
       curl -X DELETE "http://localhost:8000/api/contestants/1/"
       ```


**Desk API**
----

***Desk List***

   Returns a list of desk based on filtering criteria

* **URL**

      /api/desks/

* **Method:**

      `GET`

*  **URL Params**

     You can filter the returning list using optional arguments in get request.

     **Optional:**

     `contestant=[integer]`
     `active_node=[integer]`
     `room=[integer]`

* **Success Response:**

     On success a list of desk with their attributes is returned

      * **Code:** 200 <br />
        **Content:**
        ```
        [
            {
                "id": 1,
                "contestant": 1,
                "active_node": 1,
                "room": 1,
                "x": 0.2,
                "y": 0.2,
                "angle": 1
            },
            {
                "id": 2,
                "contestant": 2,
                "active_node": 3,
                "room": 1,
                "x": 0.3,
                "y": 0.5,
                "angle": 60
            }
        ]
        ```

* **Sample Call:**
       ```
       curl 'http://localhost:8000/api/desks/?room=1'
       ```

***Desk Creation***

   Create a new desk

* **URL**

    /api/desks/

* **Method:**

    `POST`

* **Data Params**

     Values for the new desk

     **Required:**

     `contestant=[integer]`
     `active_node=[string]`
     `room=[string]`

     **Optional:**

     `x=[float]`
     `y=[float]`
     `angle=[integer]`

* **Success Response:**

      Returns the desk created

      * **Code:** 201 Created <br />
        **Content:**
        ```
        {
            "id": 2,
            "contestant": 2,
            "active_node": 3,
            "room": 1,
            "x": 0.3,
            "y": 0.5,
            "angle": 60
        }
        ```

* **Sample Call:**
       ```
       curl -X POST -F "contestant=2" -F "active_node=3" -F "room=1" -F "x=0.3" -F "y=0.5" -F "angle=60" "http://localhost:8000/api/desks/"
       ```

***Single Desk Modification/Deletion***

   Fetch, update or delete desk

* **URL**

    /api/desks/<?desk_id>/

* **Method:**

    `GET` | `PUT` | `PATCH` | `DELETE`

* **Data Params**

     Params used for updating the node

     **Required for `PUT` and Optional for `PATCH`:**

     `contestant=[integer]`
     `active_node=[string]`
     `room=[string]`

     **Optional:**

     `x=[float]`
     `y=[float]`
     `angle=[integer]`

* **Success Response:**

      For `GET`, `PATCH`, and `PUT` returns the task:

      * **Code:** 200 OK <br />
        **Content:**
        ```
        {
            "id": 2,
            "contestant": 2,
            "active_node": 3,
            "room": 1,
            "x": 0.3,
            "y": 0.5,
            "angle": 60
        }
        ```

      OR

      If all parameters are not given in `PUT`

     * **Code:** 400 Bad Request<br />

      OR

      * **Code:** 404 Not Found <br />

      For delete returns nothing:

      * **Code:** 204 No Content <br />

* **Sample Call:**
       ```
       curl -X PUT -F "contestant=2" -F "active_node=3" -F "room=1" -F "x=0.369" -F "y=0.5" -F "angle=60" "http://localhost:8000/api/desks/2/"
       ```
       ```
       curl -X PATCH "x=0.369" "http://localhost:8000/api/desks/2/"
       ```
       ```
       curl "http://localhost:8000/api/desks/2/"
       ```
       ```
       curl -X DELETE "http://localhost:8000/api/desks/2/"
       ```
       
