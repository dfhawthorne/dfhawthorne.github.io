---
layout: default
title: 'Ch 08: Locking and Blocking'
base-url: home/reading-notes/oracle-database-transactions-and-locking-revealed/Ch08_Investigating_Undo.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'Oracle Database Transactions and Locking Revealed'
  url: home/reading-notes/oracle-database-transactions-and-locking-revealed
---

```sql
SELECT
    used_ublk
      AS num_undo_blocks
  FROM
      v$transaction t
    INNER JOIN
      v$session s
    ON t.addr = s.taddr
  WHERE
    s.sid = (
      SELECT
          sid
        FROM
          v$mystat
        WHERE
          rownum = 1
      )    
```

[ORA-1555](https://docs.oracle.com/en/error-help/db/ora-01555/index.html?r=23ai) is commonly caused by:

- undo segment is too small
- programs fetch across `COMMIT`s
- block cleanout

### Automatic UNDO Management

- Use `UNDO_RETENTION`
- Require auto-extensible `UNDO` tablespace

For fixed size `UNDO` tablespace, use _UNDO Advisor_ from `DBMS_ADVISOR`.

### Block Cleanout

Delayed block cleanout causes [ORA-1555](https://docs.oracle.com/en/error-help/db/ora-01555/index.html?r=23ai) when a block has a transaction ID stored and that transaction ID is not found in the `UNDO` tablespace.

If the transaction ID was found in the `UNDO` tablespace, then the `COMMIT` SCN could then be determined if the transaction was committed.

Since the transaction no longer exists in the `UNDO` tablespace, then the transaction must have reached a resolution: `COMMIT` or `ROLLBACK`.

MVC requires SCN.
