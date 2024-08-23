---
layout: default
title: 'Ch 02: Locking and Blocking'
base-url: home/reading-notes/oracle-database-transactions-and-locking-revealed/Ch02_Locking_and_Blocking.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'Oracle Database Transactions and Locking Revealed'
  url: home/reading-notes/oracle-database-transactions-and-locking-revealed
---

### Need for Locking

> One of the key challenges in developing multiuser database-driven applications is to maximize concurrent access and, at the same time, ensure that each user is able read and modify the data in a consistent fashion.

> Locks are mechanisms used to regulate cocurrent access to a shared resource

The following points are very important:

> All databases are fundamentally different

> You must approach each new database as if you had never used a database before.

The Oracle RDBMS allows you to:

> ...commit when you must, and not before

Use table locks in a batch process.

Lost updates are due to updating all columns in a row not just the changed ones, nor checking for original values.

### Pessimistic Locking

Pessimistic locking requires stateful connection.

```sql
SELECT ... FOR UPDATE NOWAIT
```

The above SQL can return [ORA-54](https://docs.oracle.com/en/error-help/db/ora-00054/index.html?r=23ai). The advantage is that the SQL statement returns immediately.

### Optimistic Locking

```sql
UPDATE t SET ... WHERE decode(col1,old_val,1) = 1
```

The above SQL only updates the table if the columns contain the expected values.

Avoid mixing pessimistic and optimistic locking.

Can use a version column (number or timestamp):

- via a row trigger
- best in the `UPDATE` statement
  - this is fragile in the application code
  - best to use stored procedures to encapsulate the `UPDATE`
  
Or a hash/checksum:

- `DBMS_CRYPTO.HASH`
- `DBMS_SQLHASH.GETHASH`
- `ORA_HASH`
- `STANDARD_HASH`

Can create a virtual column

### Blocking

> Blocking occurs when one session holds a lock on a resource that another session is requesting.

This could indicate a lost update bug

Blocked inserts on PK/UK

Can use a trigger to hash PK to a user lock via `DBMS_UTILITY.GET_HASH_VALUE`. Detect via `DBMS_LOCK.REQUEST`.

`SELECT FOR UPDATE NOWAIT`

- is pessimistic when user wants to update
- is optimistic just before `UPDATE` or `DELETE`

### Deadlocks

> Deadlocks occur when you have two sessions, each of which is holding a resource that the other wants.

Main cause is unindexed FK:

- updating parent's PK
- especially for generated SQL which updates every column even if the value is not changed

Deleting a row in the parent will lock the entire child table.

### Lock Escalation

Lock escalation decreases granularity of the locks. Oracle RDBMS never escalates.

Lock conversion/promotion.

