CREATE KNOWLEDGE_BASE IF NOT EXISTS demand_kb;
CREATE KNOWLEDGE_BASE IF NOT EXISTS shipment_kb;

CREATE TABLE IF NOT EXISTS sales_data (
    product_name TEXT,
    sales_date DATE,
    promotion BOOLEAN,
    season TEXT,
    sales_quantity INT
);

INSERT INTO sales_data (product_name, sales_date, promotion, season, sales_quantity)
VALUES
    ('Tea', '2024-12-01', TRUE, 'Winter', 120),
    ('Coffee', '2024-12-02', FALSE, 'Winter', 90),
    ('Tea', '2025-01-10', FALSE, 'Spring', 140),
    ('Juice', '2025-02-15', TRUE, 'Spring', 160),
    ('Tea', '2025-03-01', TRUE, 'Spring', 180);

CREATE PREDICTOR IF NOT EXISTS mindsdb.demand_forecast_predictor
FROM sales_data
PREDICT sales_quantity
USING
    product_name AS product_name,
    sales_date AS sales_date,
    promotion AS promotion,
    season AS season;

INSERT INTO mindsdb.demand_kb
SELECT * FROM sales_data;

CREATE TABLE IF NOT EXISTS shipment_data (
    origin TEXT,
    destination TEXT,
    dispatch_date DATE,
    expected_arrival_date DATE,
    traffic_conditions TEXT,
    weather_conditions TEXT,
    predicted_arrival_date DATE
);

CREATE PREDICTOR IF NOT EXISTS mindsdb.shipment_delay_predictor
FROM shipment_data
PREDICT predicted_arrival_date
USING
    origin AS origin,
    destination AS destination,
    dispatch_date AS dispatch_date,
    expected_arrival_date AS expected_arrival_date,
    traffic_conditions AS traffic_conditions,
    weather_conditions AS weather_conditions;

CREATE JOB IF NOT EXISTS update_sales_data_job
RUN EVERY 12 HOURS
AS
    INSERT INTO sales_data
    SELECT * FROM latest_demand_data_source
    WHERE sales_date > (SELECT MAX(sales_date) FROM sales_data);

CREATE AGENT IF NOT EXISTS supply_chain_agent
USING
    model = 'gemini-1.5-flash',
    google_api_key = 'YOUR_GOOGLE_API_KEY',
    include_knowledge_bases = ['mindsdb.demand_kb', 'mindsdb.shipment_kb'],
    prompt_template = '
        mindsdb.demand_kb contains sales and demand data.
        mindsdb.shipment_kb contains delivery and delay prediction data.
        Answer questions related to demand forecasting or shipment optimization.
    ';