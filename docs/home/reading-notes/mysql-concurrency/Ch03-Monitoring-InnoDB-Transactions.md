---
layout: default
title: 'Ch 03: Monitoring InnoDB Transactions'
base-url: home/reading-notes/mysql-concurrency/Ch03-Monitoring-InnoDB-Transactions.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'MySQL Concurrency'
  url: home/reading-notes/mysql-concurrency.html
---

### Information Schema INNODB_TRX

> ...most dedicated source of information about InnoDB transactions.

> Since autocommitting is enabled, there can only be one statement in the transaction (an explicit `START TRANSACTION` disables autocommitting).

INNODB can skip:

- prepare to hold back
- undo info

```text
trx_autocommit_non_locking=1
```

### InnoDBMonitor

```sql
SHOW ENGINE INNODB STATUS\G
```

### INNODB_METRICS and sys.metrics

```text
information_schema.INNODB_METRICS
   subsystem='transaction'
```

The most important metric is `trx_rseg_history_len` because it shows how far behind the purge from the undo logs is.

```sql
SELECT variable_value
    FROM sys.metrics
    WHERE
      type='InnoDB Metrics - transaction'
    AND
      variable_name='trx_rseg_history_len';
```
