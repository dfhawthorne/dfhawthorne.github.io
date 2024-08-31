---
layout: default
title: 'Ch 02: Monitoring Locks and Mutexes'
base-url: home/reading-notes/mysql-concurrency/Ch02-Monitoring-Locks-and-Mutexes.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'MySQL Concurrency'
  url: home/reading-notes/mysql-concurrency.html
---

> The Performance Schema contains the source of most of the locks information available except for deadlocks.

`metadata_locks` table

> To record information, the wait/lock/metadata/sql/model Performance Schema instrument must be enabled (it is enabled by default in MySQL 8.0).

- PK `OBJECT_INSTANCE_BEGIN` memory address of the object
  - `LOCK_TYPE`
  - `LOCK_STATUS`
    - `GRANTED`
    - `PENDING`
- `TABLE_HANDLES`
  - table locks
  - `INTERNAL_LOCK`
  - `EXTERNAL_LOCK`
- `DATA_LOCKS`
- `DATA_LOCK_WAITS`

> Data locks are at the medium level between the metadata locks and the synchronization object.

### Synchronization Waits

- most difficult to monitor
- frequent, short duration
- high overhead of monitoring
- not enabled by default

Categories:

1. cond
1. mutex
1. prlock (priority read lock)
1. rwlock (read/write lock)
1. sxlock (INNODB only for B-Tree searches)

wait/synch/mutex/innodb/dbwr_mutex

- `performance_schema.setup_instruments`
- `performance_schema.setup_consumers`

Can use `UPDATE`. Better to use configuration file.

Enabling monitoring on a production systems could cause an outage.

`event_waits_%` views - needs associated consumers to be enabled.

> Given how short lived a synchronization wait normally is and how frequently they are encountered, the summary tables are usually the most useful for investigating waits using the Performance Schema.

### Statement and Error Tables

- `EVENT_STATEMENTS_CURRENT` enabled by default
- `EVENT_STATEMENTS_HISTORY` enabled by default
- `EVENT_STATEMENTS_HISTORY_LONG` requires consumer to be enabled

```sql
SET SESSION innodb_lock_wait_timeout = <n>;
```

```text
ERROR 1205: Lock wait timeout exceeded; try restarting transaction
```

- `mysql_errno`
- `returned_sqlstate`
- `message_text`

```sql
SHOW TABLES FROM performance_schema LIKE '%error%';
```

> The `events_errors_summary_global_by_error` is populated with all known errors from the time MySQL is started even if the error has not yet been encountered. So, you can safely query for specific errors at all times including using the table to look up the error number from the name.

### SYS Schema

- `INNODB_LOCK_WAITS`
- `SCHEMA_TABLE_LOCK_WAITS`

`X$` unformatted data

### Status Counters and INNODB Metrics

> The global status counters can be found in the `performance_schema.global_status` table or with the `SHOW GLOBAL STATS` statement. The INNODB metrics are found in the `performance_schema.INNODB_METRICS` view.

- `SUBSYSTEM`
- `COMMENT`
- `TYPE` (counter, value, etc.)

INNODB mutexes/semaphores contention (`innodb_rwlock_%` metrics)

### Configuring the INNODB Metrics

- `innodb_monitor_disable`
- `innodb_monitor_enable`
- `innodb_monitor_reset`
- `innodb_monitor_reset_all`

> __Caution:__ The metrics have varying overheads, so you are recommended to test with your workload before enabling in production.
> 
> By enabling the `innodb_status_output_locks` option (disabled by default), all locks will be listed; this is similar to what you have in the Performance Schema `data_locks` table.
> 
> You generate the InnodB lock monitor output using the `SHOW INNODB STATUS` statement.
> 
> Nowadays, the lock information in the INNODB monitor output is better obtained from the `performance_schema.data_locks` and `performance_schema.data_lock_waits` tables. The deadlock information is however still very useful.

`innodb_status_option` dump info every 15 secs

`innodb_print_all_deadlocks`

### InnoDB Mutexes and Semaphores

> In InnoDB monitoring, there is no clear distinction between mutexes and semaphores.
> 
> `SHOW ENGINE INNODB MUTEX` only includes mutexes and rw-lock semaphores that has had at least one OS wait.
> 
> There is usally no reason to disable the latch metric.

