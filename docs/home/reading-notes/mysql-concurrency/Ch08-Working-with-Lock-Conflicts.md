---
layout: default
title: 'Ch 08: Working with Lock Conflicts'
base-url: home/reading-notes/mysql-concurrency/Ch08-Working-with-Lock-Conflicts.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'MySQL Concurrency'
  url: home/reading-notes/mysql-concurrency.html
---

MyISAM uses very coarse-grained locks and avoid failed locks except for time-outs - very poor write concurrency.

Fine-grained locks increases possibility of deadlocks.

## Contention-Aware Transaction Scheduling (CATS)

- MySQL 5.7- FIFO
- MySQL 8.0+ CATS

Drive transactions with a large number of locks to completion earlier in order to release a large number of locks.

Safeguard against lock starvation by inserting a barrier at end of current queue and processing all preceding requests before considering new requests.

8.0.20 CATS always used; FIFO retired.

```text
trx_schedule_weight
    information_schema.INNODB_TRX
```

### InnoDB Data Lock Compatibility

Not necessarily symmetric

Lock order is significant.

### Metadata and Backup Lock Wait

`lock_wait_timeout` defaults to 365 days.

`FLUSH TABLES`: high value better because lower levels are not cleared on timeouts.

### InnoDB Lock Wait Timeouts

Record locks are subject to timeout due to flush, metadata, or backup locks.

Default is 50 seconds for record locks.

`ER_LOCK_WAIT_TIMEOUT` 1205

`innodb_rollback_on_timeout`:

- globals (restart)
- disabled (default) only statement
- enabled (whole transaction)

Keep record lock timeouts lower than default of 20 seconds.

`innodb_lock_wait_timeout`: 1 or 2 seconds if deadlock detection disabled (also enable `innodb_rollback_on_timeout`)

### Deadlocks

With deadlock detection enabled, InnoDB chooses the transaction that has done the least work as the one to abandon.

Deadlock detection allows immediate resolution instead of waiting for timeouts.

`trx_weight` in `information_schema`; `INNODB_TRX`; More work, more weight.

Fewest locks held, more likely to be killed in deadlock resolution.

Can even get a deadlock on a single row. Can be caused by FK.

High query concurrency: turn detection off because of deadlock detection overhead.

`innodb_deadlock_detect=OFF`

Improved performance in MySQL 8.0.18+

Also:

```text
innodb_lock_wait_timeout=1
innodb_rollback_on_timeout=enabled
```

### InnoDB Mutex and Semaphore Waits

Either loop pool or suspend

> Polling allows the lock to be obtained more quickly but it keeps the CPU thread busy and polling can cause CPU cahce invalidation for other threads.

`innodb_spin_wait_delay`: Small values for fast single CPU cache; large values for multi-CPU.

`innodb_spin_wait_pause_multiplier=50` 8.0.16+ Skylake.

`innodb_sync_spin_loops=30` Number of spins before suspension.

```sql
SHOW ENGINE INNODB MUTEX
```

- When wait is greater than 240 seconds, InnoDB monitor enable, and output to error log
- When wait is greater than 600 seconds, shutdown instance

> When executing `CHECK TABLE`, the timeout threashold is increased to 7200 seconds (2 hours).


