import mindsdb_sdk as SDK
from mindsdb_sdk import connect
from django.conf import settings
import logging
from dotenv import load_dotenv
import os

load_dotenv()

logger = logging.getLogger(__name__)

class MindsDBHelper:
    def __init__(self):
        self.connection = None
        self._connect()

    def _connect(self):
        try:
            self.connection = connect(
                os.getenv('MINDSDB_HOST'),        # host
                int(os.getenv('MINDSDB_PORT')),   # port
                os.getenv('MINDSDB_USER'),        # user
                os.getenv('MINDSDB_PASSWORD')     # password
            )
        except Exception as e:
            logger.error(f"Failed to connect to MindsDB: {str(e)}")
            raise

    def predict_demand(self, product_name, sales_date, promotion, season):
        try:
            predictor = self.connection.predictors.demand_forecast_predictor
            result = predictor.predict({
                'product_name': product_name,
                'sales_date': sales_date,
                'promotion': promotion,
                'season': season
            })
            return result[0]['sales_quantity'] if result else None
        except Exception as e:
            logger.error(f"Demand prediction failed: {str(e)}")
            return None

    def predict_shipment(self, origin, destination, dispatch_date,
                         expected_arrival_date, traffic_conditions, weather_conditions):
        try:
            predictor = self.connection.predictors.shipment_delay_predictor
            result = predictor.predict({
                'origin': origin,
                'destination': destination,
                'dispatch_date': dispatch_date,
                'expected_arrival_date': expected_arrival_date,
                'traffic_conditions': traffic_conditions,
                'weather_conditions': weather_conditions
            })
            return result[0]['predicted_arrival_date'] if result else None
        except Exception as e:
            logger.error(f"Shipment prediction failed: {str(e)}")
            return None

    def query_agent(self, question):
        try:
            agent = self.connection.agents.supply_chain_agent
            result = agent.query(question)
            return result[0]['answer'] if result else None
        except Exception as e:
            logger.error(f"Agent query failed: {str(e)}")
            return None

    def execute_sql(self, query, params=None):
        try:
            return self.connection.sql(query, params)
        except Exception as e:
            logger.error(f"SQL execution failed: {str(e)}")
            return None

mdb_helper = MindsDBHelper()
