from django.db import connection

def predict_shipment_delay(origin, destination, dispatch_date, expected_arrival_date, traffic_conditions, weather_conditions):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT actual_arrival_date
            FROM mindsdb.shipment_delay_predictor
            WHERE origin=%s AND destination=%s AND dispatch_date=%s 
            AND expected_arrival_date=%s AND traffic_conditions=%s 
            AND weather_conditions=%s
        """, [origin, destination, dispatch_date, expected_arrival_date, traffic_conditions, weather_conditions])
        
        result = cursor.fetchone()
        return result[0] if result else None

def predict_demand(product_name, sales_date, promotion, season):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT sales_quantity
            FROM mindsdb.demand_forecast_predictor
            WHERE product_name=%s AND sales_date=%s AND promotion=%s AND season=%s
        """, [product_name, sales_date, promotion, season])
        
        result = cursor.fetchone()
        return result[0] if result else None
