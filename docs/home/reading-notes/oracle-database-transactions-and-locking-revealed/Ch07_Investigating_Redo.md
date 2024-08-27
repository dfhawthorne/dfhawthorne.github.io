---
layout: default
title: 'Ch 07: Investigating Redo'
base-url: home/reading-notes/oracle-database-transactions-and-locking-revealed/Ch07_Investigating_Redo.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'Oracle Database Transactions and Locking Revealed'
  url: home/reading-notes/oracle-database-transactions-and-locking-revealed
---

REDO management serialization:

- `LGWR` (`LGxx` worker on multiprocessor)
- `ARCH`
- `DG`

Larger REDO increases time

REDO is less for direct path insert than for conventional insert.

Cannot turn off REDO

```sql
SELECT forced_logging FROM v$database;
```

Significantly less REDO does not meam no REDO.

`NOLOGGING` operations are not recoverable.

`NOLOGGING` in SQL statements or in segment definitions.

Both of the following events hang the database:

1. Checkpoint not complete
1. Archival required

Other events:

- log file switch
- log buffer space
- log file switch checkpoint
- archival incomplete

### Checkpointing

Parameters:

- `FAST_START_MTTR_TARGET`
- `LOG_CHECKPOINT_INTERVAL`
- `LOG_CHECKPOINT_TIMEOUT`

### Block Clean Out

Block clean out of expired transaction locks will generate REDO

Cleanout on `COMMIT` is not completed if number of changed blocks is greater than 10% of DB cache.

> In a warehouse where you make massive `UPDATE`s to the data after a load, block cleanouts may be a factor in your design.

`DBMS_STATS` after a large `UPDATE` will do a block cleanout.

### Log File Waits

Most common causes of log file waits:

- slow device
- ORL on same device as read heavy
- mounting log device with bufferred I/O
- RAID-5

### Temporary Table

18C+ private temp table

`TEMP_UNDO_ENABLED`

pre 12C, no REDO for GTT but UNDO is logged

12C- `TEMP_UNDO_ENABLED=TRUE`

Any DML against TEMP TABLE - little or no REDO

```sql
CREATE PRIVATE TEMPORARY TABLE t
    ...
    ON COMMIT PRESERVE DEFINITION;
```

