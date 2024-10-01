---
layout: default
title: 'Autonomous Database Queries'
base-url: home/procedures/oci-procedures/identity-domains-queries.html
breadcrumbs:
- title: 'Home'
  url: index.html
- title: 'Procedures'
  url: home/procedures.html
- title: 'OCI Procedures'
  url: home/procedures/oci-procedures.html
---

# Autonomous Database Queries

## Summary

These are some OCI queries that I use for the `db autonomous-database` API.

## References

* [Oracle Cloud Infrastructure CLI Command Reference](https://docs.oracle.com/en-us/iaas/tools/oci-cli/3.43.0/oci_cli_docs/index.html)
  * [iam](https://docs.oracle.com/en-us/iaas/tools/oci-cli/3.43.0/oci_cli_docs/cmdref/iam.html)
    * [compartment](https://docs.oracle.com/en-us/iaas/tools/oci-cli/3.43.0/oci_cli_docs/cmdref/iam/compartment.html)
      * [list](https://docs.oracle.com/en-us/iaas/tools/oci-cli/3.43.0/oci_cli_docs/cmdref/iam/compartment/list.html)
  * [db](https://docs.oracle.com/en-us/iaas/tools/oci-cli/3.43.0/oci_cli_docs/cmdref/db.html)
    * [autonomous-database](https://docs.oracle.com/en-us/iaas/tools/oci-cli/3.43.0/oci_cli_docs/cmdref/db/autonomous-database.html)
      * [delete](https://docs.oracle.com/en-us/iaas/tools/oci-cli/3.43.0/oci_cli_docs/cmdref/db/autonomous-database/delete.html)
      * [list](https://docs.oracle.com/en-us/iaas/tools/oci-cli/3.43.0/oci_cli_docs/cmdref/db/autonomous-database/list.html)
  * [work-requests](https://docs.oracle.com/en-us/iaas/tools/oci-cli/3.43.0/oci_cli_docs/cmdref/work-requests.html)
    * [work-request](https://docs.oracle.com/en-us/iaas/tools/oci-cli/3.43.0/oci_cli_docs/cmdref/work-requests/work-request.html)
      * [get](https://docs.oracle.com/en-us/iaas/tools/oci-cli/3.43.0/oci_cli_docs/cmdref/work-requests/work-request/get.html)

## List Autonomous Databases

To list autonomous databases in the `Sandbox` compartment, run the following command:

```bash
export OCI_SANDBOX_OCID=$(   \
    oci iam compartment list \
        --query 'data[0].id' \
        --name 'Sandbox'     \
        --raw-output         \
    )
oci db autonomous-database list \
    --compartment-id $OCI_SANDBOX_OCID \
    --query 'data[*].{"DB Name": "db-name", "Display Name": "display-name", "DB Version": "db-version", "DB Workload": "db-workload", "ID": "id"}' \
    --output table
```

The sample output is:

```text
+-----------+------------+-------------+--------------------------+-------------------------------------------------------------------------------------------------------+
| DB Name   | DB Version | DB Workload | Display Name             | ID                                                                                                    |
+-----------+------------+-------------+--------------------------+-------------------------------------------------------------------------------------------------------+
| SANDBOX02 | 19c        | OLTP        | Sandbox_DB_02            | ocid1.autonomousdatabase.oc1.ap-sydney-1.anzxsljr63mv4jya4oms24aer32jlizpmvnc4wfn4codgdlrqmwlwurereia |
| sandbox01 | 19c        | OLTP        | Sandbox_Autonomous_DB_01 | ocid1.autonomousdatabase.oc1.ap-sydney-1.anzxsljr63mv4jya7q2pnq5v3ogz3efp4ya564ds2je64p6uuvwxsphgu5ha |
+-----------+------------+-------------+--------------------------+-------------------------------------------------------------------------------------------------------+
```

__NOTE:__ The `--raw-output` option is needed to remove double quotes ('"') from the data returned by the `iam compartment list` API call. The presence of the double quotes causes the following error on the `db autonomous-database list` API call:

```text
ServiceError:
{
    "client_version": "Oracle-PythonSDK/2.126.4, Oracle-PythonCLI/3.41.0",
    "code": "InvalidParameter",
    "logging_tips": "Please run the OCI CLI command using --debug flag to find more debug information.",
    "message": "Invalid compartmentId",
    "opc-request-id": "BA57A92130C34B31A32C570312893D1C/FDEF72D198604F072EAEBDA469858E2A/E57071EA1C4461B5A11F5645C7ED32D6",
    "operation_name": "list_autonomous_databases",
    "request_endpoint": "GET https://database.ap-sydney-1.oraclecloud.com/20160918/autonomousDatabases",
    "status": 400,
    "target_service": "database",
```

The debug output shows, in part:

```text
Not using Expect header...
send: b'GET /20160918/autonomousDatabases?compartmentId=%22ocid1.compartment.oc1..aaaaaaaamoo6uz2qmix2adls2cgoqxxhdt4wuam3wbcrw6co6z4osweos6da%22 HTTP/1.1\r\nuser-agent:
```

The double quotes ('"') are encoded as '%22' in the string above.

## Delete Autonomous Database (Asynchronous)

Run the following commands to delete the `Sandbox_Autonomous_DB_01` autonomous DB asynchronously in the `Sandbox` compartment:

```bash
export OCI_SANDBOX_OCID=$(   \
    oci iam compartment list \
        --query 'data[0].id' \
        --name 'Sandbox'     \
        --raw-output         \
    )
export OCI_SANDBOX01_OCID=$(                      \
    oci db autonomous-database list               \
        --compartment-id $OCI_SANDBOX_OCID        \
        --display-name 'Sandbox_Autonomous_DB_01' \
        --query 'data[0].id'                      \
        --raw-output                              \
    )
oci db autonomous-database delete                \
    --autonomous-database-id $OCI_SANDBOX01_OCID \
    --force
```

The use of the `--force` option suppresses the following prompt:

```text
Are you sure you want to delete this resource? [y/N]: 
```

The sample output is:

```text
{
  "opc-work-request-id": "ocid1.coreservicesworkrequest.oc1.ap-sydney-1.abzxsljripp2ojmpp3jfuttxvlhpnmnxgzcyzgcrutsy5pjwbd46fvqsrtsq"
}
```

Run the following command to show the status of the work request:

```bash
oci work-requests work-request get \
    --work-request-id ocid1.coreservicesworkrequest.oc1.ap-sydney-1.abzxsljripp2ojmpp3jfuttxvlhpnmnxgzcyzgcrutsy5pjwbd46fvqsrtsq
```

Sample output is:

```text
{
  "data": {
    "compartment-id": "ocid1.compartment.oc1..aaaaaaaamoo6uz2qmix2adls2cgoqxxhdt4wuam3wbcrw6co6z4osweos6da",
    "id": "ocid1.coreservicesworkrequest.oc1.ap-sydney-1.abzxsljripp2ojmpp3jfuttxvlhpnmnxgzcyzgcrutsy5pjwbd46fvqsrtsq",
    "operation-type": "Delete Autonomous Database",
    "percent-complete": 100.0,
    "resources": [
      {
        "action-type": "DELETED",
        "entity-type": "autonomousDatabase",
        "entity-uri": "/20160918/autonomousDatabases/ocid1.autonomousdatabase.oc1.ap-sydney-1.anzxsljr63mv4jya7q2pnq5v3ogz3efp4ya564ds2je64p6uuvwxsphgu5ha",
        "identifier": "ocid1.autonomousdatabase.oc1.ap-sydney-1.anzxsljr63mv4jya7q2pnq5v3ogz3efp4ya564ds2je64p6uuvwxsphgu5ha"
      }
    ],
    "status": "SUCCEEDED",
    "time-accepted": "2024-06-08T18:10:12.830000+00:00",
    "time-finished": "2024-06-08T18:11:33.030000+00:00",
    "time-started": "2024-06-08T18:10:20.800000+00:00"
  }
}
```

## Delete Autonomous Database (Synchronous)

Run the following commands to delete the `Sandbox_DB_02` autonomous DB synchronously in the `Sandbox` compartment:

```bash
export OCI_SANDBOX_OCID=$(   \
    oci iam compartment list \
        --query 'data[0].id' \
        --name 'Sandbox'     \
        --raw-output         \
    )
export OCI_SANDBOX02_OCID=$(               \
    oci db autonomous-database list        \
        --compartment-id $OCI_SANDBOX_OCID \
        --display-name 'Sandbox_DB_02'     \
        --query 'data[0].id'               \
        --raw-output                       \
    )
oci db autonomous-database delete                \
    --autonomous-database-id $OCI_SANDBOX02_OCID \
    --force                                      \
    --wait-for-state SUCCEEDED
```

The sample output is:

```text
Action completed. Waiting until the work request has entered state: ('SUCCEEDED',)
{
  "data": {
    "compartment-id": "ocid1.compartment.oc1..aaaaaaaamoo6uz2qmix2adls2cgoqxxhdt4wuam3wbcrw6co6z4osweos6da",
    "id": "ocid1.coreservicesworkrequest.oc1.ap-sydney-1.abzxsljrhdnxkaajlngvv4ywpa2q5owep4bvkuby5muxgli5onesfygtgu5a",
    "operation-type": "Delete Autonomous Database",
    "percent-complete": 100.0,
    "resources": [
      {
        "action-type": "DELETED",
        "entity-type": "autonomousDatabase",
        "entity-uri": "/20160918/autonomousDatabases/ocid1.autonomousdatabase.oc1.ap-sydney-1.anzxsljr63mv4jya4oms24aer32jlizpmvnc4wfn4codgdlrqmwlwurereia",
        "identifier": "ocid1.autonomousdatabase.oc1.ap-sydney-1.anzxsljr63mv4jya4oms24aer32jlizpmvnc4wfn4codgdlrqmwlwurereia"
      }
    ],
    "status": "SUCCEEDED",
    "time-accepted": "2024-06-08T18:28:23.919000+00:00",
    "time-finished": "2024-06-08T18:29:39.992000+00:00",
    "time-started": "2024-06-08T18:28:27.140000+00:00"
  }
}
```
