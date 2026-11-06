# Depop BI Engine

A pipeline that turns my Depop sales export into a BigQuery table so I can
decide what to list, how to price it, and what sells fastest.

**Pipeline:** Depop CSV → Python (pandas) cleaning → BigQuery → SQL

## Key findings (51 completed sales, Jun–Nov 2026)

**1. Higher-priced items earn most of the revenue without selling slower.**
7 items priced $20+ brought in $236.80, about 42% of revenue from 14% of
sales. Items under $6 took the longest to sell (35 days on average) versus
25 days for $10–19.99 items. Underpricing didn't speed up sales.

| Price band | Sold | Revenue | Avg days to sell |
|---|---|---|---|
| Under $6 | 12 | $55.01 | 35.3 |
| $6–9.99 | 24 | $174.85 | 29.3 |
| $10–19.99 | 8 | $92.70 | 25.4 |
| $20+ | 7 | $236.80 | 28.3 |

**2. Typical tops sell in about 3 weeks.** The median is 19 days; the average
(35.9) is pulled up by one top that sat for 136 days, so I report the median.

| Category | Sold | Revenue | Median days | Longest |
|---|---|---|---|---|
| Tops | 35 | $296.76 | 19 | 136 |
| Footwear | 3 | $130.00 | 4 | 11 |
| Bottoms | 6 | $52.30 | 1 | 30 |
| Coats and jackets | 2 | $50.00 | 53 | 116 |
| Accessories | 5 | $30.30 | 4 | 8 |

**3. Refunds:** 6 of 57 sales (about 11%) were refunded, including 2 of 9
sales over $20.

**Decisions:** list fewer, higher-value items; add detailed measurements and
condition photos to $20+ listings to cut refunds; list jackets in fall.

## Data decisions
See [docs/decision_log.md](docs/decision_log.md): handling items with no
cost, buyer privacy, refunds, and bundles.

## Limitations
- 35 sales is a small sample; the footwear result rests on 3 sales and
  is a pattern to test, not a rule.
- The export only includes sold items, so sell-through rate isn't measured.
- All items are from my own closet, so revenue ≈ gross profit before fees.

## Tools
Python (pandas), Google BigQuery, SQL, Git
