---
layout: default
title: 'Ch 03: Locks, Latches, and Mutexes'
base-url: home/reading-notes/oracle-database-transactions-and-locking-revealed/Ch03_Locks_Latches_and_Mutexes.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'Oracle Database Transactions and Locking Revealed'
  url: home/reading-notes/oracle-database-transactions-and-locking-revealed
---

DML Locks

### TX (Transaction)

Transaction ID = Segment #, Slot, Sequence #

- `V$TRANSACTION`
  - `XIDUSN`
  - `XIDSLOT`
  - `XIDSQN`
- `V$SESSION`
- `V$LOCK`
  - `ID1`
    - Top 16 bits refer to the rollback segment
    - Bottom 16 bits refer to the slot
  - `ID2` is the sequence number

`LMODE` = 6 exclusive

`DBA_WAITERS`

Insufficient transaction slots in a block will cause [ORA-54](https://docs.oracle.com/en/error-help/db/ora-00054/index.html?r=23ai) (resource busy) even if no one else has locked the row.

`INITRANS` defaults to 2 even though Data Dictionary shows 1 for tables.

### TM (DML Equeue)

> TM locks are used to ensure that the structure of a table is not altered while you are modifying its contents.

For Oracle 11.2+, `DDL_LOCK_TIMEOUT`

### AE (Edition Lock)

TM ID1 = Object ID

Setting `DML_LOCKS` = 0 means no DDL allowed.

```sql
ALTER TABLE t DISABLE TABLE LOCK
```

- Prevents DDL on table t
- Can also detect full table lock resulting from an unindexed FK.

### DDL

In Oracle RDBMS, DDL always commit.

Lock Type | Description
--- | ---
Exclusive | Table R/O
Shareable | Protects structures, allows DML
Breakable Parse | Notification to plans

### DL (Direct Load)

Prevent direct load during online index creation

### OD (Online DDL)

11G +

`DBA_DDL_LOCKS` created through `catblock.sql`

Cannot DCL on executing procedures

### Latches

> Latches are lightweight serialisation devices used to coordinate multiuser access to shared data structures, objects, and files.

Miss count

Mutex is a lightweight latch but with less functionality.

### Manual Locking

- `SELECT FOR UPDATE`
- `LOCK TABLE` does not prevent DML lock
- `LOCK TABLE IN EXCLUSIVE MODE`

`DBMS_LOCK`

