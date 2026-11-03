# Decision Log

## 1. Source and cost columns loaded as null (2026-10-29)
Depop's export has no cost field. Most items came from my own closet,
so I added `source` (closet / thrifted / purchased) and `acquisition_cost`
(0.00 for closet items) instead of estimating costs, which would invent data.

## 2. Raw export broke BigQuery (2026-10-29)
Descriptions span multiple lines, money had $ signs and Excel `="-"` values,
and the file included buyer names and addresses. Wrote clean_depop.py to
remove personal data, normalize money and dates, and use snake_case columns.

## 3. Refunds (2026-11-02)
3 of 38 sales were refunded. Revenue queries exclude them with
`WHERE refunded_to_buyer_amount = 0`.

## 4. Bundles and SKU (2026-11-02)
SKU was never filled in on Depop, so I dropped it. Bundle counts were blank
for single items and for later rows of a bundle; set to 1 and 0 so the
column sums to total items sold (38).

## 5. Sandbox limits (2026-11-02)
BigQuery's free sandbox requires tables to expire within 60 days.
Tables are rebuilt from the cleaned CSV, so the pipeline is repeatable.
