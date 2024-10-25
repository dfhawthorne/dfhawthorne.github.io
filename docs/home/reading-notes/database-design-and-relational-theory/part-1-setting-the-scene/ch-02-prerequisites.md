---
layout: default
title: 'Ch 02: Prerequisites'
base-url: home/reading-notes/database-design-and-relational-theory/part-1-setting-the-scene/ch-02-prerequisites.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'Database Design and Relational Theory: Normal Forms and All That Jazz'
  url: home/reading-notes/database-design-and-relational-theory.html
- title: 'Part 1 Setting the Scene'
  url: home/reading-notes/database-design-and-relational-theory/part-1-setting-the-scene.html
---

## Overview

> Any given database consists of relation variables (rekvars for short)
>
> ...
>
> The value of any given relvar at any given time is a relation value (relation for short)
>
> ...
>
> Every relvar represents a certain predicate
>
> ...
>
> Within any given relvar, every tuple represents a certain proposition.
>
> ...
>
> In accordance with the _the Closed World Assumption_, relvar __R__ at time __T__ contains all and only those tuples that represent instantiations of the predicate corresponding to relvar __R__ that evaluate to __TRUE__ at time __T__.
>
> ...
>
> ...relations have two parts, a heading and a body. Basically the heading is a set of attributes, and the body is a set of tuple that conform to that heading.

Both RELVARs and RELATIONs have headings.

The heading of a RELVAR represents a predicate which in the intended meaning.

> ...a predicate isn't really a statement as such, rather, it's the assetion made by that statement.

Propositions can be true or false.
