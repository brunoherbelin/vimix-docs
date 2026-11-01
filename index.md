---
layout: default
title: vimix documentation
---

Community documentation for [vimix](https://github.com/brunoherbelin/vimix).
Want to add a page? Read [how to contribute](https://github.com/brunoherbelin/vimix-docs/blob/master/CONTRIBUTING.md).

{% assign docs = site.pages | where_exp: "p", "p.path contains 'pages/'" | sort: "title" %}
{% for p in docs %}
- [{{ p.title }}]({{ p.url | relative_url }}): {{ p.summary }}
  <small>by {{ p.author }}, vimix {{ p.vimix_version }}, {{ p.date | date: "%Y-%m-%d" }}</small>
{% endfor %}
