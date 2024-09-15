---
layout: default
title: 'Ch 18: Case Study: Semaphores'
base-url: home/reading-notes/mysql-concurrency/Ch18-Case-Study-Semaphores.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'MySQL Concurrency'
  url: home/reading-notes/mysql-concurrency.html
---

Mutex and semaphore contention is very elusive.

Overall added latency and throughput reduction.

## The Symptoms

INNODB Monitor - SEMAPHORES

`innodb_rqlock_%` InnoDB metrics.

## The Cause

> The issue is that requests for a shared resource, such as access to the adaptive hash index, arrive faster than they can be handled. These resources are protected inside the source code using mutexes and rw-locks. Contention indicates that either you have hit the concurrency limit of the MySQL version you are using for your workload or that your need to split the resource into more parts or similar.

## The Investigation

```text
information_schema.INNODB_METRICS
sys.metrics
  innodb_rwlock_%
  - shared/S-X/X
  #spin waits
  #spin rounds
  #o/s waits
```

OS Waits increase when spin rounds is greater than `innodb_sync_spin_loops` (default 80).

> Here the number of spin waits is almost constant during the test, but the number of spin rounds (the top line in the graph) greatly increases around 7 seconds into the test. This also causes the number of OS waits to increase. That the OS waits jump up means that the spin rounds for a spin wait exceed `innodb_sync_spin_loops` (defaults to 30).

```sql
SHOW ENGINE INNODB STATUS\G
  SEMAPHORES
SHOW ENGINE INNODB MUTEX;
```

> If you do not have access monitoring data for the queries executed during the time of contention, you can try to monitor the queries using sys.session or the Performance Schema tables with statement information (`threads`, `events_statements_current`, `events_statements_history`, and `events_statements_history_long`). An option is also to use the `statement_performance_analyzer()` procedure in the `sys` schema which takes two snapshots of the `events_statements_summary_by_digest` table and calculates the difference and returns one or more reports showing information about the queries executed between the two snapshots.

## The Solution and Prevention

- Disabling the adpative hash index altogether
- Increasing the number of partitions
- Increasing the number of spin rounds before suspending the thread
- Splitting the workload to different replicas

```text
adaptive_hash_searches
adaptive_hash_searches_btree
innodb_adpative_hash_index_parts

INSERT BUFFER AND ADAPTIVE HASH INDEX section of STATUS report
```
