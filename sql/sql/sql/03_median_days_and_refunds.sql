SELECT date_of_sale, brand, item_price, refunded_to_buyer_amount
FROM `depop-data-pipeline.depop_sales.sales_v2`
WHERE refunded_to_buyer_amount > 0;
