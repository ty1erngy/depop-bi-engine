# Depop BI Engine

A pipeline that turns my Depop sales export into a BigQuery table so I can
decide what to list, how to price it, and what sells fastest.

**Pipeline:** Depop CSV → Python (pandas) cleaning → BigQuery → SQL

## Key finding
Across 35 completed sales (Jun–Aug 2026), 3 pairs of shoes brought in $130,
65% as much revenue as 21 tops ($201), and sold in 5.3 days on average
versus 12 days for tops.

| Category | Sold | Revenue | Avg price | Avg days to sell |
|---|---|---|---|---|
| Tops | 21 | $200.90 | $9.57 | 12.0 |
| Footwear | 3 | $130.00 | $43.33 | 5.3 |
| Bottoms | 6 | $52.30 | $8.72 | 10.7 |
| Accessories | 5 | $30.30 | $6.06 | 4.4 |

**Decision:** prioritize sourcing and listing footwear; bundle or reprice
tops that sit longer than two weeks.

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
