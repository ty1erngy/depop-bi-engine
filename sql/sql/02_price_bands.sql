SELECT
  category,
  COUNT(*) AS items_sold,
  APPROX_QUANTILES(DATE_DIFF(date_of_sale, date_of_listing, DAY), 2)[OFFSET(1)] AS median_days_to_sell,
  MAX(DATE_DIFF(date_of_sale, date_of_listing, DAY)) AS longest_days
FROM `depop-data-pipeline.depop_sales.sales_v2`
WHERE refunded_to_buyer_amount = 0
GROUP BY category
ORDER BY items_sold DESC;
