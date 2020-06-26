# 2Queue Branch.
-run api.py
-To start Redis open docker desktop and run `docker run -p6379:6379 redis`.
-if you have a database, delete it
-run csv-import.py to add to queue
-check medis and the database: it should have products in but nothing else
-To start the worker for emtying the reviewer q: `rq worker reviewer`: now db has product and reviewers

-wait till all reviewers are added then restart the docker
-run `docker run -p6379:6379 redis`
-run csv-import2.py
-To start the worker for emtying the review q2: `rq worker review`
-tada