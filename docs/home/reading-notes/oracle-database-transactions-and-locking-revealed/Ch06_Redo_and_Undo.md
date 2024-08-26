---
layout: default
title: 'Ch 06: Redo and Undo'
base-url: home/reading-notes/oracle-database-transactions-and-locking-revealed/Ch06_Redo_and_Undo.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'Oracle Database Transactions and Locking Revealed'
  url: home/reading-notes/oracle-database-transactions-and-locking-revealed
---

> Database restore and recovery is the one thing that a DBA is not allowed to get wrong.

`ARCn` copies online redo log (ORL) to archived redo log files.

> Without redo logs the database would not offer any more protection than a filesystem.

Each node in a RAC has its own ORL and UNDO tablespace.

> The database is logically restored to the way it was -- any changes are logically undone -- but the data structures, the database blocks themselves, may well be different after a rollback.

Deferred segment creation (default 11.2+)

Undo segments are protected by REDO.

> Before `DBWn` can write any of the blocks that are changed to disk, `LGWR` must flush (to disks) the REDO information related to those blocks.

This includes to the UNDO needed in case of database failure during an incomplete transaction.

Crash recovery - roll forward all REDO then rollback all incomplete transactions.

ORL not read except for archival during normal processing.

> A `COMMIT` is generally a very fast operation, regardless of the transaction size.

`COMMIT`:

- Generates SCN
- LGWR flushes REDO
- Release locks
- Remove transaction
- Block cleanout

PL/SQL commit opt suspended for distributed transaction, and DG in maximum available mode.

Would this be implied by maximum protection mode?

Rollbacks are expensive.

