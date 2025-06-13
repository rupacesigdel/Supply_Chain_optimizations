from mindsdb_sdk import connect

mdb = connect()

def predict_demand(product_name, sales_date, promotion, season):
    try:
        predictor = mdb.get_predictor('demand_forecast_predictor')

        result = predictor.predict({
            'product_name': product_name,
            'sales_date': sales_date,
            'promotion': promotion,
            'season': season
        })

        return result[0]['sales_quantity']
    except Exception as e:
        print("Prediction error (demand):", str(e))
        return None

def predict_shipment_delay(origin, destination, dispatch_date, expected_arrival_date, traffic_conditions, weather_conditions):
    try:
        predictor = mdb.get_predictor('shipment_delay_predictor')

        result = predictor.predict({
            'origin': origin,
            'destination': destination,
            'dispatch_date': dispatch_date,
            'expected_arrival_date': expected_arrival_date,
            'traffic_conditions': traffic_conditions,
            'weather_conditions': weather_conditions
        })

        return result[0]['actual_arrival_date']
    except Exception as e:
        print("Prediction error (shipment):", str(e))
        return None
