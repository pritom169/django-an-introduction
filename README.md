# Storefront (Django Demo)

A compact Django e‑commerce demo I used for myself to teach **ORM basics**, **Admin customization**, **generic relations (tags)**, and **PostgreSQL**. Deep tutorials can be found in **`django-part1/README.md`**.

## Features

### Django Part 1

- **Apps**: `store` (products, orders, customers) and `tags` (generic tagging via `GenericForeignKey`).
- **Admin**:
  - Custom list pages (`list_display`, `list_filter`, `search_fields`, `actions`).
  - Inline editing (`OrderItemInline`) and **generic** inline (`GenericTabularInline` for `TaggedItem`).
  - Safe override of the base queryset (`get_queryset`) with annotations.
- **ORM**: examples of filtering, `Q`/`F` expressions, `select_related`/`prefetch_related`, aggregation & annotation, and raw SQL when needed.
- **Dev tooling**: optional Django Debug Toolbar.
