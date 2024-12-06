---
layout: default
title: 'WAF Protection Capabilities Queries'
base-url: home/procedures/oci-procedures/waf-protection-capabilities-queries.html
breadcrumbs:
- title: 'Home'
  url: index.html
- title: 'Procedures'
  url: home/procedures.html
- title: 'OCI Procedures'
  url: home/procedures/oci-procedures.html
---

## Summary

Web Application Firewall (WAF) protection capabilities are grouped by various tags. This example lists all such protections that are:

- The latest version
- Tagged as for Cross-Site Scripting (XSS)

## Procedure

```bash
compartment_id=... # Set Compartment OCID
waf_tag=$(                                                      \
    oci waf protection-capability                               \
        list-protection-capability-group-tags                   \
        --compartment-id ${compartment_id}                      \
        --all                                                   \
        --query "data.items[?contains(name,'XSS')].name | [0]"  \
    )
oci waf protection-capability list                              \
    --compartment-id ${compartment_id}                          \
    --all                                                       \
    --group-tag "${waf_tag}"                                    \
    --is-latest-version true                                    \
    --query 'data.items[*].{key:key,Description:description}'   \
    --sort-by key                                               \
    --sort-order ASC                                            \
    --output table
```

Sample output is:

```text
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------+
| Description                                                                                                                                                            | key       |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------+
| WordPress Rencontre plugin allows Cross Site Scripting attack via rencontre_widget.php                                                                                 | 201950708 |
| Cisco Jabber protocol vulnerable to cross-site scripting                                                                                                               | 202156845 |
| Cisco Jabber protocol vulnerable to cross-site scripting                                                                                                               | 202156846 |
| Cross-Site Scripting (XSS) Attempt: XSS Filters - Category 1.                                                                                                          | 9410000   |
| Cross-Site Scripting (XSS) Attempt: Detects XSS Libinjection                                                                                                           | 941100    |
| Cross-Site Scripting (XSS) Attempt: On Referer Header XSS Attack Detected via libinjection                                                                             | 941101    |
| Cross-Site Scripting (XSS) Attempt: XSS Filters - Category 1. Script tag based XSS vectors, e.g., <script> alert(1)</script>                                           | 941110    |
| Cross-Site Scripting (XSS) Attempt: XSS Filters - Category 2. XSS vectors making use of event handlers like onerror, onload etc, e.g., <body onload="alert(1)">        | 941120    |
| Cross-Site Scripting (XSS) Attempt: XSS Filters - Category 3. XSS vectors making use of Attribute Vectors                                                              | 941130    |
| Cross-Site Scripting (XSS) Attempt: XSS Filters - Category 4. XSS vectors making use of javascript URI and tags, e.g., <p style="background:url(javascript:alert(1))"> | 941140    |
| Cross-Site Scripting (XSS) Attempt: XSS Filters - Category 5. HTML attribues - src, style and href                                                                     | 941150    |
| Cross-Site Scripting (XSS) Attempt: NoScript XSS Filters, NoScript InjectionChecker - HTML injection                                                                   | 941160    |
| Cross-Site Scripting (XSS) Attempt: NoScript XSS Filters, NoScript InjectionChecker - Attributes injection                                                             | 941170    |
| Cross-Site Scripting (XSS) Attempt: Blacklist Keywords from Node-Validator                                                                                             | 941180    |
| Cross-Site Scripting (XSS) Attempt: Blacklist Keywords from Node-Validator                                                                                             | 941181    |
| Cross-Site Scripting (XSS) Attempt: XSS Filters from IE                                                                                                                | 941190    |
| Cross-Site Scripting (XSS) Attempt: XSS Filters from IE                                                                                                                | 941200    |
| Cross-Site Scripting (XSS) Attempt: XSS Filters from IE                                                                                                                | 941210    |
| Cross-Site Scripting (XSS) Attempt: XSS Filters from IE                                                                                                                | 941220    |
| Cross-Site Scripting (XSS) Attempt: XSS Filters from IE                                                                                                                | 941230    |
| Cross-Site Scripting (XSS) Attempt: XSS Filters from IE                                                                                                                | 941240    |
| Cross-Site Scripting (XSS) Attempt: XSS Filters from IE                                                                                                                | 941250    |
| Cross-Site Scripting (XSS) Attempt: XSS Filters from IE                                                                                                                | 941260    |
| Cross-Site Scripting (XSS) Attempt: XSS Filters from IE                                                                                                                | 941270    |
| Cross-Site Scripting (XSS) Attempt: XSS Filters from IE                                                                                                                | 941280    |
| Cross-Site Scripting (XSS) Attempt: XSS Filters from IE                                                                                                                | 941290    |
| Cross-Site Scripting (XSS) Attempt: XSS Filters from IE                                                                                                                | 941300    |
| Cross-Site Scripting (XSS) Attempt: US-ASCII encoding bypass listed on XSS filter evasion                                                                              | 941310    |
| Cross-Site Scripting (XSS) Attempt: HTML Tag Handler                                                                                                                   | 941320    |
| Cross-Site Scripting (XSS) Attempt: XSS Filters from IE                                                                                                                | 941330    |
| Cross-Site Scripting (XSS) Attempt: XSS Filters from IE                                                                                                                | 941340    |
| Cross-Site Scripting (XSS) Attempt: UTF-7 encoding XSS filter evasion for IE                                                                                           | 941350    |
| Cross-Site Scripting (XSS) Attempt: Defend against JSFuck and Hieroglyphy obfuscation of Javascript code.                                                              | 941360    |
| Cross-Site Scripting (XSS) Attempt: Prevent 94118032 bypass by using JavaScript global variables                                                                       | 941370    |
| Cross-Site Scripting (XSS) Attempt: Defend against AngularJS client side template injection                                                                            | 941380    |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------+
```
