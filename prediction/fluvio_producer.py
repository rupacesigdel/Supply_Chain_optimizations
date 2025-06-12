from fluvio_producer  import Fluvio
import json

def produce_shipment_data():
    fluvio = Fluvio.connect()
    producer = fluvio.topic_producer("shipment-data")

    shipment = {
        "origin": "Warehouse A",
        "destination": "Location B",
        "dispatch_date": "2024-09-15T10:00:00",
        "expected_arrival_date": "2024-09-20T12:00:00",
        "traffic_conditions": "heavy",
        "weather_conditions": "rain"
    }
    
    producer.send(str(json.dumps(shipment)))

def produce_sales_data():
    fluvio = Fluvio.connect()
    producer = fluvio.topic_producer("sales-data")

    sales = {
        "product_name": "Product A",
        "sales_date": "2024-09-15",
        "promotion": True,
        "season": "Autumn",
        "sales_quantity": 100
    }

    producer.send(str(json.dumps(sales)))
