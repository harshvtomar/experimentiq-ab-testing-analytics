PRAGMA foreign_keys = ON;
DROP VIEW IF EXISTS arm_kpis;
DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
 row_id TEXT PRIMARY KEY,
 recency INTEGER NOT NULL CHECK(recency BETWEEN 1 AND 12),
 history_segment TEXT NOT NULL,
 history REAL NOT NULL CHECK(history>=0),
 mens INTEGER NOT NULL CHECK(mens IN(0,1)),
 womens INTEGER NOT NULL CHECK(womens IN(0,1)),
 zip_code TEXT NOT NULL CHECK(zip_code IN('Urban','Rural','Surburban','Suburban')),
 newbie INTEGER NOT NULL CHECK(newbie IN(0,1)),
 channel TEXT NOT NULL CHECK(channel IN('Phone','Web','Multichannel')),
 segment TEXT NOT NULL CHECK(segment IN('No E-Mail','Mens E-Mail','Womens E-Mail')),
 visit INTEGER NOT NULL CHECK(visit IN(0,1)),
 conversion INTEGER NOT NULL CHECK(conversion IN(0,1)),
 spend REAL NOT NULL CHECK(spend>=0),
 arm TEXT NOT NULL CHECK(arm IN('Control','Men''s email','Women''s email')),
 geography TEXT NOT NULL CHECK(geography IN('Urban','Rural','Suburban')),
 history_band_order INTEGER NOT NULL CHECK(history_band_order BETWEEN 1 AND 7),
 spend_cents INTEGER NOT NULL CHECK(spend_cents>=0),
 CHECK(arm=CASE segment WHEN 'No E-Mail' THEN 'Control' WHEN 'Mens E-Mail' THEN 'Men''s email' ELSE 'Women''s email' END)
);
CREATE INDEX ix_arm ON customers(arm);
CREATE INDEX ix_channel_arm ON customers(channel,arm);
CREATE VIEW arm_kpis AS
 SELECT arm, COUNT(*) AS n, SUM(conversion) AS conversions, SUM(visit) AS visits,
 SUM(spend_cents) AS spend_cents,
 1.0*SUM(conversion)/NULLIF(COUNT(*),0) AS conversion_rate,
 1.0*SUM(visit)/NULLIF(COUNT(*),0) AS visit_rate,
 SUM(spend_cents)/100.0 AS total_spend,
 SUM(spend_cents)/100.0/NULLIF(COUNT(*),0) AS spend_per_customer
 FROM customers GROUP BY arm;
