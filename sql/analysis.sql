-- query: 01_assignment_counts
SELECT arm,n,100.0*n/SUM(n) OVER() AS assigned_pct FROM arm_kpis ORDER BY arm;

-- query: 02_conversion_rates
SELECT arm,n,conversions,conversion_rate FROM arm_kpis ORDER BY arm;

-- query: 03_visit_rates
SELECT arm,n,visits,visit_rate FROM arm_kpis ORDER BY arm;

-- query: 04_observed_spending
SELECT arm,n,total_spend,spend_per_customer FROM arm_kpis ORDER BY arm;

-- query: 05_treatment_vs_control
WITH control AS (SELECT * FROM arm_kpis WHERE arm='Control')
SELECT t.arm,t.n,c.n AS control_n,100*(t.conversion_rate-c.conversion_rate) AS conversion_difference_pp,
100*(t.conversion_rate/NULLIF(c.conversion_rate,0)-1) AS conversion_relative_pct,
100*(t.visit_rate-c.visit_rate) AS visit_difference_pp,
t.spend_per_customer-c.spend_per_customer AS spend_difference_dollars
FROM arm_kpis t CROSS JOIN control c WHERE t.arm<>'Control';

-- query: 06_recency
SELECT recency,arm,COUNT(*) AS n,AVG(conversion) AS conversion_rate, SUM(spend_cents)/100.0/COUNT(*) AS spend_per_customer FROM customers GROUP BY recency,arm HAVING COUNT(*)>0 ORDER BY recency,arm;

-- query: 07_history_segments
SELECT history_band_order,history_segment,arm,COUNT(*) AS n,AVG(conversion) AS conversion_rate,AVG(history) AS mean_historical_spend FROM customers GROUP BY history_band_order,history_segment,arm ORDER BY history_band_order,arm;

-- query: 08_geography
SELECT geography,arm,COUNT(*) AS n,AVG(conversion) AS conversion_rate,AVG(visit) AS visit_rate FROM customers GROUP BY geography,arm ORDER BY geography,arm;

-- query: 09_channel
SELECT channel,arm,COUNT(*) AS n,AVG(conversion) AS conversion_rate, SUM(spend_cents)/100.0/COUNT(*) AS spend_per_customer FROM customers GROUP BY channel,arm ORDER BY channel,arm;

-- query: 10_customer_tenure
SELECT CASE newbie WHEN 1 THEN 'New in past 12 months' ELSE 'Existing before past 12 months' END AS tenure,arm,COUNT(*) AS n,AVG(conversion) AS conversion_rate FROM customers GROUP BY newbie,arm ORDER BY newbie,arm;

-- query: 11_baseline_purchases
SELECT arm,COUNT(*) AS n,SUM(CASE WHEN mens=1 AND womens=1 THEN 1 ELSE 0 END) AS bought_both,AVG(mens) AS historical_mens_share,AVG(womens) AS historical_womens_share FROM customers GROUP BY arm ORDER BY arm;

-- query: 12_channel_composition
WITH cells AS (SELECT channel,arm,COUNT(*) AS n FROM customers GROUP BY channel,arm) SELECT channel,arm,n,100.0*n/SUM(n) OVER(PARTITION BY arm) AS within_arm_pct FROM cells ORDER BY arm,channel;
