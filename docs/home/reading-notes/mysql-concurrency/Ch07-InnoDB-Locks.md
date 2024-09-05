---
layout: default
title: 'Ch 07: InnoDB Locks'
base-url: home/reading-notes/mysql-concurrency/Ch07-InnoDB-Locks.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'MySQL Concurrency'
  url: home/reading-notes/mysql-concurrency.html
---

All locks in [Ch 06](home/reading-notes/mysql-concurrency/Ch06-High-Level-Locks-Types.html) were general for MySQL.

### Record Locks and Next-Key Locks

Next key lock is a combination of record lock and a gap lock -- default for INNODB.

Exclusive for tranactions with exception.

`performance_schema.data_locks`

`X,REC_NO_GAP` = exclusive on row, not gap

### Gap Locks

> A gap lock protects the space between two record.

This is for clustered or secondary index.

Psuedo records | infinum | before first
 | supremum | after last

`UPDATE` `INSERT`

Gap lock protects the space where new rows would be inserted.

`X,GAP` ensures no new rows are inserted after the current row which is being modified.

No conflict between gap locks

- does not prevent access to gap
- stops insert into a gap

### Predicate and Page Locks

predicate locks are the equivalent of gap locks for spatial indexes

in RR and `SERIALIZABLE`

minimum bounding rectangle (MBR)

`performance_schema.data_locks`

- `PREDICATE`
- `PRDT_PAGE`

### Insert Intention Locks

INNODB has insert intention locks in addition to MySQL's IS and IX locks.

is a gap lock

### Auto-Increment Locks

`innodb_auto_lock_mode=0|1|2`

MySQL 8+ - 2 is the default (requires restart)

0 | Tranditional | MySQL 5.0-
1 | Consectutive | when #rows is known, use mutex, else traditional
2 | Interleaved | No lock. Bin log disabled or `binlog_format=row` (default MySQL 8+)

### Mutexes and RW-Lock Semaphores

INNODB uses mutex and semaphores interchangeably

MySQL:

- mutex protects internal code paths
- semaphores serialised application code paths using MySQL

```sql
SHOW ENGINE INNODB STATUS
SHOW ENGINE INNODB MUTEX
```


