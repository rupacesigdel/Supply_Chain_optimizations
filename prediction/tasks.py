from celery import shared_task
from django.core.mail import send_mail
from .mindsdb_utils import predict_shipment_delay
from django.db import connection

@shared_task
def check_for_shipment_delays():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT origin, destination, dispatch_date, expected_arrival_date, traffic_conditions, weather_conditions
            FROM shipment_data
        """)
        shipments = cursor.fetchall()
        
        for shipment in shipments:
            predicted_arrival = predict_shipment_delay(
                shipment[0], shipment[1], shipment[2], shipment[3], shipment[4], shipment[5]
            )
            
            if predicted_arrival > shipment[3]:
                send_mail(
                    'Shipment Delay Alert',
                    f'Shipment from {shipment[0]} to {shipment[1]} is expected to be delayed.',
                    'admin@example.com',
                    ['user@example.com']
                )
