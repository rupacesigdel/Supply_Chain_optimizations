CREATE KNOWLEDGE_BASE demand_kb;

CREATE TABLE sales_data (
    product_name TEXT,
    sales_date DATE,
    promotion BOOLEAN,
    season TEXT,
    sales_quantity INT
);

INSERT INTO sales_data (product_name, sales_date, promotion, season, sales_quantity)
VALUES
    ('Tea',    '2024-12-01', TRUE,  'Winter', 120),
    ('Coffee', '2024-12-02', FALSE, 'Winter', 90),
    ('Tea',    '2025-01-10', FALSE, 'Spring', 140),
    ('Juice',  '2025-02-15', TRUE,  'Spring', 160),
    ('Tea',    '2025-03-01', TRUE,  'Spring', 180);

CREATE PREDICTOR mindsdb.demand_forecast_predictor
FROM sales_data
PREDICT sales_quantity
USING
    product_name AS product_name,
    sales_date AS sales_date,
    promotion AS promotion,
    season AS season;


CREATE JOB update_sales_data_job
RUN EVERY 12 HOURS
AS
    INSERT INTO sales_data
    SELECT * FROM latest_demand_data_source
    WHERE sales_date > (SELECT MAX(sales_date) FROM sales_data);
