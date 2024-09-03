---
layout: default
title: 'Ch 06: High Level Locks Types'
base-url: home/reading-notes/mysql-concurrency/Ch06-High-Level-Locks-Types.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'MySQL Concurrency'
  url: home/reading-notes/mysql-concurrency.html
---

### User Level Locks

```text
GET_LOCK
IS_FREE_LOCK
IS_USED_LOCK
RELEASE_ALL_LOCKS
RELEASE_LOCK
```

```sql
SELECT * FROM metadata_locks
  WHERE objecttype = 'USER LEVEL LOCK';
```

Lock duration of `EXPLICIT` - must be cleared by user.

```sql
SELECT release_all_locks();
```

### Flush Locks

Backups

`FLUSH TABLES` until end of statement. If `WITH READ LOCK`, until explicitly freed/

> An implicit table flush is also triggered at the end of the `ANALYZE TABLE` statement.

Long running queries cause issues. Cannot complete `FLUSH TABLES` while a query is running.

`lock_wait_timeout` seconds. If greater, request abandoned.

`TDC` (table definition cache) not released until query completes. May need to kill query.

> Waiting for table flush

### Metadata Locks

MySQL 5.5+

Protects schema:

- `SELECT/DML` shared
- DDL exclusive

> Waiting for table metadata lock

`OPTIMIZE TABLE` does not change the structure of a table but it is a DDL and thus requires the metadata lock.

State = committed as MySQL does not have transactional DDL

```sql
SELECT *
  FROM performance_schema.metadata_locks
  WHERE object_type = 'TABLE';
```

Can be requested explicitly through a `LOCK TABLE`.

### Explicit Table Locks

```text
LOCK TABLE - shared or exclusive
FLUSH TABLES WITH READ LOCK - always shared
```

need `UNLOCK TABLES`

With explicit locks, you are restricted to the mode requested (read only for shared; read/write for exclusive) and to those tables you have locked.

```text
ER_TABLE_NOT_LOCKED_FOR_WRITE
ER_TABLE_NOT_LOCKED
```

### Implicit Table Locks

query takes implicit table locks

INNODB:

- table locks: flush; metadata; explicit
- has intention locks at table level

| Statement | Lock Level |
| --- | --- |
| `SELECT FOR SHARE` | IS |
| `SELECT FOR UPDATE` | IX |
| DML | IX |
| FK | IS in parent |

```sql
SELECT *
  FROM performance_schema.data_locks
  WHERE lock_type = 'TABLE';
```

### Backup Locks

- Instance Level lock
- MySQL 8+
- Prevents inconsistent backups
- Prevents
  - Create; rename; or remove files
  - account management
  - DDL that do not log to READ

```sql
LOCK INSTANCE FOR BACKUP;
UNLOCK INSTANCE;
```

Requires `BACKUP_ADMIN` privilege

```sql
SELECT *
  FROM performance_schema.metadata_locks
  WHERE object_type = 'BACKUP LOCK';
```

### Log Locks

- MySQL 5.7- global read lock for log positions, GTID
- MySQL8+ log lock instead
- GTID Global Transaction ID

Prevents changes to log-related information e.g. commits, `FLUSH LOGS`, etc.

> The log lock is taken implicitly by querying the `performance_schema.log_status` table.

