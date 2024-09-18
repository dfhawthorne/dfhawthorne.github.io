---
layout: default
title: '03. Server Core Installation'
base-url: home/reading-notes/pro-sql-server-2019-admin/part-1-installation-and-configuration/03-server-core-installation.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'Pro SQL Server 2019 Adminstration'
  url: home/reading-notes/pro-sql-server-2019-admin.html
- title: 'Part I. Installation and Configuration'
  url: home/reading-notes/pro-sql-server-2019-admin/part-1-installation-and-configuration.html
---

Windows Server Core only allows CLI.

Run `setup.exe` under PowerShell

```text
/IACCEPTSQLSERVERLICENCETERMS
/ACTION
/FEATURES
/ROLE
/INSTANCENAME
/SQLSYSADMINACCOUNTS
/AGTSVCACCOUNT
/SQLSVCACCOUNT
/qs unattended installation
```

Available actions:

- `install`
- `upgrade`
- `prepareimage`
- `completeimage`
- `InstallFailoverCluster`
- `PrepareFailoverCluster`
- `CompleteFailoverCluster`
- `AddNode`
- `RemoveNode`

```ps
.\setup.exe
Get-Service-DisplayName "instance"
Select objectname, displayname,status
```

Install sqlserver module (individual|SSMS) or download from PS Gallery

```ps
Find Module sqlserver
Install-Module sqlserver
Invoke-Sqlcmd -serverinstance "host\inst" - query "SELECT @@SERVERNAME"

## Troubleshooting

```text
pgm file\Microsoft SQL Server\150\
    Setup Bootstrap\Log\
        Summary.txt
        YYYYMMDD_HHMM\
            Detail.txt
            System Configuration Check Report.txt
```

```text
find /i error exceptionDatastore settings.xml
    config files
    *.log "Return value 3"
    some of them are expected
```

Product Update replaces deprecated slipstream functionality (install).

SS 2017 - no more SP, only CU and GDR:

- CU Cumulative Update
- GDR Genral distribution release - security hot fixes

To use product update:

```text
/UPDATEENABLED=1 or True
/UPDATESOURCE=
    Microsoft Update
    WSUS service
    release patch
    UNC of N/W share
```

Allows installation to apply CU in build

```text
$parameters = @[
    ServerInstance = '...'
    Query = "SELECT @@SERVERNAME,@@VERSION"
    ]
```

Invoke -sqlcmd @parameters

Can mix configuration file and command parameters.

