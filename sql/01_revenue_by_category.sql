SELECT
  category,
  COUNT(*) AS items_sold,
  ROUND(SUM(item_price), 2) AS revenue,
  ROUND(AVG(item_price), 2) AS avg_price,
  ROUND(AVG(DATE_DIFF(date_of_sale, date_of_listing, DAY)), 1) AS avg_days_to_sell
FROM `depop-data-pipeline.depop_sales.sales_v2`
WHERE refunded_to_buyer_amount = 0
GROUP BY category
ORDER BY revenue DESC;
