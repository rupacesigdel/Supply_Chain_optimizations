from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from django.contrib import messages
from mindsdb_sdk import connect
from .mindsdb_utils import mdb_helper
import logging
import os

logger = logging.getLogger(__name__)


def initialize_database():
    """Initialize database tables using predict.sql"""
    try:
        sql_path = os.path.join(os.path.dirname(__file__), 'predict.sql')
        with open(sql_path, 'r') as f:
            sql_commands = f.read().split(';')

        with connection.cursor() as cursor:
            for command in sql_commands:
                if command.strip():
                    cursor.execute(command)

        logger.info("✅ Database initialized successfully.")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {str(e)}")


def dashboard(request):
    question = None
    answer = None
    chat_history = request.session.get('chat_history', [])

    if request.method == 'POST' and 'question' in request.POST:
        question = request.POST.get('question')
        try:
            mdb = connect('http://127.0.0.1:47334')
            agent = mdb.agents.supply_chain_agent
            result = agent.query(question)
            answer = result[0]['answer'] if result else "I couldn't find an answer."

            chat_history.append({'question': question, 'answer': answer})
            if len(chat_history) > 10:
                chat_history = chat_history[-10:]
            request.session['chat_history'] = chat_history

        except Exception as e:
            answer = f"Agent error: {str(e)}"
            logger.error(f"Agent query failed in dashboard: {e}")
            messages.error(request, answer)

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM shipment_data ORDER BY dispatch_date DESC LIMIT 10")
            recent_shipments = cursor.fetchall()

            cursor.execute("SELECT * FROM sales_data ORDER BY sales_date DESC LIMIT 10")
            recent_sales = cursor.fetchall()

        context = {
            'recent_shipments': recent_shipments,
            'recent_sales': recent_sales,
            'question': question,
            'answer': answer,
            'chat_history': chat_history
        }
        return render(request, 'prediction/dashboard.html', context)

    except Exception as e:
        return render(request, 'prediction/dashboard.html', {
            'error': str(e),
            'question': question,
            'answer': answer,
            'chat_history': chat_history
        })


def demand_forecasting(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        sales_date = request.POST.get('sales_date')
        promotion = request.POST.get('promotion') == 'on'
        season = request.POST.get('season')

        try:
            predicted_sales = mdb_helper.predict_demand(product_name, sales_date, promotion, season)
            return render(request, 'prediction/demand_result.html', {'predicted_sales': predicted_sales})
        except Exception as e:
            return render(request, 'prediction/demand_result.html', {'error': str(e)})

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
            predicted_arrival_date = mdb_helper.predict_shipment(
                origin, destination, dispatch_date, expected_arrival_date,
                traffic_conditions, weather_conditions
            )
            return render(request, 'prediction/shipment_result.html', {'predicted_arrival_date': predicted_arrival_date})
        except Exception as e:
            return render(request, 'prediction/shipment_result.html', {'error': str(e)})

    return render(request, 'prediction/shipment_form.html')


def inventory_optimization(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM inventory_data ORDER BY product_name")
            inventory = cursor.fetchall()

        low_inventory = [item for item in inventory if item[1] < item[2]]

        return render(request, 'prediction/inventory_optimization.html', {
            'inventory': inventory,
            'low_inventory': low_inventory,
        })

    except Exception as e:
        return render(request, 'prediction/inventory_optimization.html', {'error': str(e)})


def create_demand_predictor():
    try:
        mdb_helper.connection.predictors.create(
            name='demand_forecast_predictor',
            predict='sales_quantity',
            from_data='sales_data'
        )
    except Exception as e:
        logger.error(f"Error creating predictor: {str(e)}")


def list_predictors():
    try:
        predictors = mdb_helper.connection.predictors.list()
        print(predictors)
    except Exception as e:
        print(f"Error listing predictors: {str(e)}")


def check_predictor():
    try:
        predictor = mdb_helper.connection.predictors.get('demand_forecast_predictor')
        print("Predictor found:", predictor)
    except Exception as e:
        print("Error:", str(e))


def agent_query(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        try:
            mdb = connect('http://127.0.0.1:47334')
            agent = mdb.agents.supply_chain_agent
            result = agent.query(question)
            answer = result[0]['answer'] if result else "No answer from agent."

            return render(request, 'prediction/agent_response.html', {
                'question': question,
                'answer': answer
            })
        except Exception as e:
            logger.error(f"Agent query failed: {e}")
            messages.error(request, f"Error querying agent: {str(e)}")
            return render(request, 'prediction/agent_form.html')

    return render(request, 'prediction/agent_form.html')


if os.environ.get('RUN_INIT_DB', 'True') == 'True':
    initialize_database()
