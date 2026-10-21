-- Independent arithmetic on named inputs, never on rounded display values.
WITH base AS (
 SELECT *, audience * source_effect * multiplier AS revenue,
 audience * delivery_cost AS variable_cost
 FROM scenario_inputs
), contribution AS (
 SELECT *, revenue * margin AS gross_contribution,
 variable_cost + fixed_cost AS total_cost FROM base
)
SELECT treatment, revenue, gross_contribution, variable_cost, total_cost,
 gross_contribution-total_cost AS net_value,
 audience*multiplier*margin*source_low-total_cost AS net_low,
 audience*multiplier*margin*source_high-total_cost AS net_high,
 total_cost/NULLIF(audience*margin,0) AS break_even_uplift,
 CASE WHEN revenue>0 THEN total_cost/revenue END AS break_even_margin,
 source_effect*multiplier*margin-fixed_cost/NULLIF(audience*1.0,0) AS max_delivery_cost,
 (gross_contribution-total_cost)/NULLIF(total_cost,0) AS net_return_on_cost
FROM contribution;
