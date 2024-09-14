---
layout: default
title: 'Ch 17: Case Study: Foreign Keys'
base-url: home/reading-notes/mysql-concurrency/Ch17-Case-Study-Foreign-Keys.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'MySQL Concurrency'
  url: home/reading-notes/mysql-concurrency.html
---

Concurrent workloads in MySQL Shell are not thread safe.

Very difficult yo simulate and diagnose.

Look for:

- metadata locks
- lock timeouts
- deadlocks

Schema knowledge can misloead during diagnosis. Look at actual locks.

> __Note__ Foreign keys are a bigger issue with metadata locks than for InnoDB record locks as the latter only affect cases where the columns used in foreign keys are involved.

With FK, set `lock_wait_timeout` low; also reduce `max_write_lock_count`.

May have to remove FK in some cases.

Handle errors as they happen to clean up resources quickly.
