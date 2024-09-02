---
layout: default
title: 'Ch 04: Transactions in the Performance Schema'
base-url: home/reading-notes/mysql-concurrency/Ch04-Transactions-in-the-Performance-Schema.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'MySQL Concurrency'
  url: home/reading-notes/mysql-concurrency.html
---

> The Performance Schema supports transaction monitoring in MySQL 5.7 and later, and it is enabled by default in MySQL 8.

```text
events_transactions_current
events_transactions_history
events_transactions_history_long
```

Abandoned transactions prevent purge of undo logs.

### Transaction Summary Tables

```text
event_transactions_summary_by_event_name
event_transactions_summary_by_account_by_event_name
event_transactions_summary_by_host_by_event_name
event_transactions_summary_by_thread_by_event_name
event_transactions_summary_by_user_by_event_name
```

R/O:

```sql
START TRANSACTION READ ONLY;
```

> When INNODB determines that an autocommiting single-statement transaction can be treated as a read-only transaction, that is still counting toward the read-write statistics in the Performance Schema.


