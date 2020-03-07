title: MongoDB CLI Intro
date: 2020-03-07 12:27
category: Database
tags: mongodb, cli
slug: mongodb-cli-intro
author: Martin Uribe
summary: Quick introduction on how to connect to a mondoDB database through the built in mongo cli application

# MongoDB CLI Intro

After publishing my article on [How to install MongoDB on Linux]({filename}how-to-install-mongodb-on-linux.md) I realized that I should have covered how to access it through the command line!
Didn't occur to me that anyone reading it might not want to download and install [Robo 3T](https://robomongo.org/)!

Sorry about that!

### Intro into the mongo cli app

It's simple enough.
Now I'm no expert but this is what I discovered just playing around with it.

```
(base) ➜  ~ mongo
MongoDB shell version v4.2.3
connecting to: mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb
Implicit session: session { "id" : UUID("39eaf67e-7de5-4874-ba3e-a6673080cfbc") }
MongoDB server version: 4.2.3
Welcome to the MongoDB shell.
For interactive help, type "help".
For more comprehensive documentation, see
	http://docs.mongodb.org/
Questions? Try the support group
	http://groups.google.com/group/mongodb-user
Server has startup warnings: 
2020-03-06T20:35:19.314-0600 I  STORAGE  [initandlisten] 
2020-03-06T20:35:19.314-0600 I  STORAGE  [initandlisten] ** WARNING: Using the XFS filesystem is strongly recommended with the WiredTiger storage engine
2020-03-06T20:35:19.314-0600 I  STORAGE  [initandlisten] **          See http://dochub.mongodb.org/core/prodnotes-filesystem
2020-03-06T20:35:22.538-0600 I  CONTROL  [initandlisten] 
2020-03-06T20:35:22.539-0600 I  CONTROL  [initandlisten] ** WARNING: Access control is not enabled for the database.
2020-03-06T20:35:22.539-0600 I  CONTROL  [initandlisten] **          Read and write access to data and configuration is unrestricted.
2020-03-06T20:35:22.539-0600 I  CONTROL  [initandlisten] 
---
Enable MongoDB's free cloud-based monitoring service, which will then receive and display
metrics about your deployment (disk utilization, CPU, operation statistics, etc).

The monitoring data will be available on a MongoDB website with a unique URL accessible to you
and anyone you share the URL with. MongoDB may use this information to make product
improvements and to suggest MongoDB products and deployment options to you.

To enable free monitoring, run the following command: db.enableFreeMonitoring()
To permanently disable this reminder, run the following command: db.disableFreeMonitoring()
---

>
```

As you can tell, I haven't secured the database yet.
Let's continue exploring though and see what the *help* command will show us.

```
> help
	db.help()                    help on db methods
	db.mycoll.help()             help on collection methods
	sh.help()                    sharding helpers
	rs.help()                    replica set helpers
	help admin                   administrative help
	help connect                 connecting to a db help
	help keys                    key shortcuts
	help misc                    misc things to know
	help mr                      mapreduce

	show dbs                     show database names
	show collections             show collections in current database
	show users                   show users in current database
	show profile                 show most recent system.profile entries with time >= 1ms
	show logs                    show the accessible logger names
	show log [name]              prints out the last segment of log in memory, 'global' is default
	use <db_name>                set current database
	db.foo.find()                list objects in collection foo
	db.foo.find( { a : 1 } )     list objects in foo where a == 1
	it                           result of the last line evaluated; use to further iterate
	DBQuery.shellBatchSize = x   set default number of items to display on shell
	exit
>
```

Ok, looks simple enough. That *show dbs* sounds interesting.

```
> show dbs
admin      0.000GB
config     0.000GB
local      0.000GB
snake_bnb  0.000GB
>
```

Ok, I see the *snake_bnb* database that we created during the [MongoDB Quickstart](https://freemongodbcourse.com/) tutorial.
Let's see what's in it with that `use <db_name>` command, followed by `show collections`.

```
> use snake_bnb
switched to db snake_bnb
> show collections
owners
>
```

Now if I reference the *help* command again, I see that I can use `db.foo.find()` to do a dump of everything in it.

```
> db.owners.find()
{ "_id" : ObjectId("5e6243ca45ed06e7f09781fc"), "registered_date" : ISODate("2020-03-06T06:36:26.108Z"), "name" : "clamytoe", "email" : "clamytoe@gmail.com", "snake_ids" : [ ], "cage_ids" : [ ] }
>
```

If I had more entries, it looks like I could search for specific entries with `db.foo.find( { a : 1 } )`.
I only have one record, so I should just get the same result as the previous command.

```
> db.owners.find( {"name": "clamytoe"} )
{ "_id" : ObjectId("5e6243ca45ed06e7f09781fc"), "registered_date" : ISODate("2020-03-06T06:36:26.108Z"), "name" : "clamytoe", "email" : "clamytoe@gmail.com", "snake_ids" : [ ], "cage_ids" : [ ] }
>
```

To exit, we just use the *exit* command.

```
> exit
bye
(base) ➜  ~
```

## Conclusion

There you have it.
A quick intro into using the *mongo* cli app.
Simple enough for quick exploration of your databases.
I'll probably be spending more time in *Robo 3T* though.
Not only can your explore the databases through a GUI, but you can also easily add, delete, and update and entries with it.
