# Storefront (Django Demo)

A compact Django e‑commerce demo I used for myself to teach **ORM basics**, **Admin customization**, **generic relations (tags)**, and **PostgreSQL**. This README is a short, practical guide. Deep tutorials can be found in **`docs/tutorial.md`**.

## Table of Contents

- [Features](#features)
- [Project Setup](#project-setup)
- [Creation of the Apps](#creation-of-the-apps)
- [Views)](#views)
- [Admin Preview](#admin-preview)
- [Troubleshooting](#troubleshooting)
- [Further Reading](#further-reading)

---

## Features

- **Apps**: `store` (products, orders, customers) and `tags` (generic tagging via `GenericForeignKey`).
- **Admin**:
  - Custom list pages (`list_display`, `list_filter`, `search_fields`, `actions`).
  - Inline editing (`OrderItemInline`) and **generic** inline (`GenericTabularInline` for `TaggedItem`).
  - Safe override of the base queryset (`get_queryset`) with annotations.
- **ORM**: examples of filtering, `Q`/`F` expressions, `select_related`/`prefetch_related`, aggregation & annotation, and raw SQL when needed.
- **Dev tooling**: optional Django Debug Toolbar.
