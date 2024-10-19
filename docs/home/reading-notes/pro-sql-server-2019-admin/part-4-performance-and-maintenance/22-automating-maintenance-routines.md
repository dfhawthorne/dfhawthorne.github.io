---
layout: default
title: '22. Automating Maintenance Routines'
base-url: home/reading-notes/pro-sql-server-2019-admin/part-4-performance-and-maintenance/22-automating-maintenance-routines.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'Pro SQL Server 2019 Adminstration'
  url: home/reading-notes/pro-sql-server-2019-admin.html
- title: 'Part IV. Performance and Maintenance'
  url: home/reading-notes/pro-sql-server-2019-admin/part-4-performance-and-maintenance
---

_SQL Server Agent_ is a service that provides the ability to create automated routines with decision-based logic and schedule to run them one time only, on a recurring basis, when _SQL Server Agent_ starts, or when a CPU idle condition occurs.

Schedules:

- one time
- when _SQL Server Agent_ starts
- CPU idle
- recurring

__Operator__ - individual or team who receives notification of job status or alert notified via e-mail, pager, and `NET SEND`. Pager and `NET SEND` are deprecated. Need to configure DB mail.

Jobs

- one or more actions (aka job steps)
- action (except T-SQL) runs under _SQL Server Agent_ account or proxy which is linked to a credential
- action can have retries
- on success/failure
- schedule: specific/shared
- notifications

Alerts repond to events

`msdb.dbo.sysalerts_performance-counters_view`

MSDB:

- _SQLAgentUserRole_
- _SQLAgentReaderRole_
- _SQLAgentOperatorRole_

`sysadmin` gets all of these roles. Not all SQL Agent activities are covered by these roles.

T-SQL run as user (no proxy)

Credential -\> proxy account -\> schedule operator used to receive e-mail 

```sql
EXEC sp_configure 'show advanced options',1;
GO
RECONFIGURE
GO
EXEC sp_configure 'Database Mail XPs',1;
GO
RECONFIGURE
GO
```

Can have a default profile which sends e-mail to one or more operators

- _Normal_ - log errors
- _Extended_ - error, warn, info
- _Verbose_ - error, warn, info, success, internal

After configuring DB mail, create operator who receives e-mails in event of job failures. Then create job.

```sql
sp_start_job @job_name=N'...';

sp_start_job @job_name=N'...' @step_name=N'...';
```

Multiserver jobs:

- __MSX__ Master Server
- __TSX__ Target Server

Use `regedit` to set `AllowDownloadedJobsToMatchProxyName` `MsxEncryotChannelOptions` registry key:

- =1 encrypt, no certificate valid
- =2 encrypt plus SSL certified
- =0 off

```sql
connect server\instance
CREATE CREDENTIAL ...;
EXEC msdb.dbo.sp_add_proxy ...;
EXEC msdb.dbo.sp_grant_proxy_to_subsystem ...;

EXEC sp_delete_jobserver
EXEC sp_add_jobserver
```

Force poll TSX -\> MSX to distributed list for latest jobs

- Defection (deleting) removes TSX.
- Synchronize Clocks MSX -\> all TSX

> SQL Server Agent is a scheduling engine for SQL Server that allows you to create powerful maintenance jobs, whith decision based logic on a variety of schedules. A job is a container for the tasks that should be performed, and each of these tasks is known as a step. Job step can have different accounts/subsystems.

Good security: proxy accounts -\> credentials -\> AD principal
