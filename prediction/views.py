from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from .mindsdb_utils import predict_demand, predict_shipment_delay
import mindsdb_sdk  as SDK
from mindsdb_sdk import connect

def dashboard(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM shipment_data ORDER BY dispatch_date DESC LIMIT 10")
            recent_shipments = cursor.fetchall()

            cursor.execute("SELECT * FROM sales_data ORDER BY sales_date DESC LIMIT 10")
            recent_sales = cursor.fetchall()

        context = {
            'recent_shipments': recent_shipments,
            'recent_sales': recent_sales,
        }
        return render(request, 'prediction/dashboard.html', context)

    except Exception as e:
        return render(request, 'prediction/dashboard.html', {'error': str(e)})

def demand_forecasting(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        sales_date = request.POST.get('sales_date')
        promotion = request.POST.get('promotion') == 'on'
        season = request.POST.get('season')

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT sales_quantity AS predicted
                    FROM mindsdb.demand_forecast_predictor
                    WHERE product_name=%s AND sales_date=%s AND promotion=%s AND season=%s
                """, [product_name, sales_date, promotion, season])
                result = cursor.fetchone()
                predicted_sales = result[0] if result else 'N/A'
        except Exception as e:
            return render(request, 'prediction/demand_result.html', {'error': str(e)})

        context = {'predicted_sales': predicted_sales}
        return render(request, 'prediction/demand_result.html', context)

    return render(request, 'prediction/demand_form.html')

def shipment_prediction(request):
    if request.method == 'POST':
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
        dispatch_date = request.POST.get('dispatch_date')
        expected_arrival_date = request.POST.get('expected_arrival_date')
        traffic_conditions = request.POST.get('traffic_conditions')
        weather_conditions = request.POST.get('weather_conditions')

        try:
            mdb = SDK()
            predictor = mdb.predictors.get('shipment_delay_predictor')

            prediction = predictor.predict({
                'origin': origin,
                'destination': destination,
                'dispatch_date': dispatch_date,
                'expected_arrival_date': expected_arrival_date,
                'traffic_conditions': traffic_conditions,
                'weather_conditions': weather_conditions
            })

            predicted_arrival_date = prediction['predicted_arrival_date'] if prediction else 'N/A'

        except Exception as e:
            return render(request, 'prediction/shipment_result.html', {'error': str(e)})

        context = {'predicted_arrival_date': predicted_arrival_date}
        return render(request, 'prediction/shipment_result.html', context)

    return render(request, 'prediction/shipment_form.html')

def inventory_optimization(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM inventory_data ORDER BY product_name")
            inventory = cursor.fetchall()

        low_inventory = [item for item in inventory if item[1] < item[2]]

        context = {
            'inventory': inventory,
            'low_inventory': low_inventory,
        }
        return render(request, 'prediction/inventory_optimization.html', context)

    except Exception as e:
        return render(request, 'prediction/inventory_optimization.html', {'error': str(e)})

def create_demand_predictor():
    mdb = SDK()
    mdb.predictors.create(
        name='demand_forecast_predictor',
        predict='sales_quantity',
        from_data='sales_data'
    )

def list_predictors():
    mdb = SDK()
    predictors = mdb.predictors.list()
    print(predictors)

def check_predictor():
    try:
        mdb = SDK()
        predictor = mdb.predictors.get('demand_forecast_predictor')
        print("Predictor found:", predictor)
    except Exception as e:
        print("Error:", str(e))

import mysql.connector
from django.shortcuts import render

def agent_query(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        try:
            conn = mysql.connector.connect(
                host='mindsdb',
                port=47335,
                user='mindsdb',
                password='',
                database='mindsdb'
            )
            cursor = conn.cursor()
            query = f"""
                SELECT answer
                FROM supply_chain_agent
                WHERE question = '{question}'
            """
            cursor.execute(query)
            result = cursor.fetchone()
            answer = result[0] if result else "No answer from agent."
            cursor.close()
            conn.close()
        except Exception as e:
            answer = f"Error querying MindsDB agent: {str(e)}"

        return render(request, 'prediction/agent_response.html', {
            'question': question,
            'answer': answer
        })

    return render(request, 'prediction/agent_form.html')
