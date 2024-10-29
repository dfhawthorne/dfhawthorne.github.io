---
layout: default
title: 'Ch 03: Normalization: Some Generalities'
base-url: home/reading-notes/database-design-and-relational-theory/part-2-functional-dependencies-boycecodd-normal-form-and-related-matters/ch-03-normalization-some-generalities.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'Database Design and Relational Theory: Normal Forms and All That Jazz'
  url: home/reading-notes/database-design-and-relational-theory.html
- title: 'Part 2 Functional Dependencies, Boyce/Codd Normal Form, and Related Matters'
  url: home/reading-notes/database-design-and-relational-theory/part-2-functional-dependencies-boycecodd-normal-form-and-related-matters.html
---

> Second, the decomposition process is basically a processof taking projections...

Nonloss is not strictly the same as information equivalent.

Normalisation is done against RELVARs

EQD Equality Dependency

Update anomaly is usually caused by FD

- Insertion anomaly
- Deletion anomaly
- Modification anomaly

> In general, BCNF is the solution to the problems caused by the kinds of anomalies listed above.

Higher level of normalisation =\> more redunancies and fewer update anomalies.

- FD =\> BCNF
- JD =\> 5NF

Decomposition adds constraints (multi-RELVAR)

Normal form is equivalent to canonical form of data.
