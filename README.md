
# Supply Chain Optimization Dashboard

## Overview
This project is a Django-based web application designed to provide insights and prediction related to supply chain management. It integrates MindsDB for machine learning prediction, allowing users to forecast demand, predict shipment delays, and optimize inventory levels.

## Contain

- [Features](#features)
- [Demo Video](#demo-video)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Demo Video
[Watch the demo video]()


## Features

1. **Dashboard for Monitoring and Insights**
   - Displays recent shipment data and sales records in a clean, easy-to-read format.
   
2. **Shipment Delay Prediction**
   - Predicts potential delays in shipment arrivals based on historical data, traffic, and weather conditions.

3. **Demand Forecasting**
   - Predicts future product demand based on historical sales data, promotions, and seasons using MindsDB's machine learning models.

4. **Inventory Optimization**
   - Provides an overview of current inventory levels, highlighting products that are running low.


## Technologies Used
- Python
- Django
- MindsDB 24.7.1.0
- PostgreSQL (for Django database and MindsDB integration)

  
## Installation

### Setting Up Your Environment

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/rupacesigdel/Supply_Chain_optimizations.git
    cd Supply-Chain-Optimizations
    ```

2. **Create a Virtual Environment:**

    ```bash
    python -m venv myenv
    source .venv/Scripts/activate  # On windows
    ```
    ```bash
    python3 -m venv myenv
    source myenv/bin/activate # On macOS/Linux:
    ```

3. **Upgrade pip (if needed):**

    ```bash
    pip install --upgrade pip
    ```

4. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```


## Project Structure
- supply_chain_optimizations/
- ├── supply_chain_management/             
- │   ├── __init__.py
- │   ├── asgi.py
- │   ├── celery.py                   
- │   ├── settings.py
- │   ├── urls.py
- │   └── wsgi.py
- ├── prediction/                        
- │   ├── __init__.py
- │   ├── admin.py
- │   ├── apps.py
- │   ├── forms.py
- │   ├── mindsdb_utils.py
- │   ├── models.py
- │   ├── tasks.py                   
- │   ├── test.py                   
- │   └──templates/prediction/
- │ -     ├── index.html
- │ -       ├── shipment_form.html
- │ -       ├── shipment_result.html
- │ -       ├── inventory_optimization.html
- │ -       ├── demand_form.html
- │ -      └── demand_result.html
- │   ├── urls.py                         
- │   └── views.py                   
- │
- ├── static/                           
- │
- ├── dockerfile
- ├── manage.py
- ├── predict.sql
- └── requirements.txt    



## Usage
1. **Start the Development Server:**

    ```sh
    python manage.py runserver
    ```
    OR :
    ```sh
    docker-compose up --build
    ```

2. **Access the Web Application:**

    Open your web browser and navigate to,
    Access:
   - Django App: `http://localhost:8000`

   - MindsDB GUI: `http://localhost:47334`

3. **Supply Chain Optimization**:
    - The application predicts shipment delays based on origin, destination, traffic conditions, and weather using **MindsDB**. This helps logistics and e-commerce platforms optimize their shipping processes by anticipating potential delays.

4. **Demand Forecasting**:
    - Using historical sales data, promotions, and seasonal patterns, the system predicts product demand. This feature is crucial for ensuring optimal stock levels and preparing for seasonal sales spikes or drops.

5. **Inventory Optimization**:
    - By predicting future demand and comparing it to current stock levels, the system suggests optimal inventory quantities, helping businesses reduce excess inventory and avoid stockouts.
      
6. **Predictive Modeling**:
    - Leveraging **MindsDB**, the platform uses machine learning models to predict shipment arrival times and sales forecasts, providing actionable insights that help businesses plan more effectively.


## Contributing

1. **Fork the Repository:**

    - Create a fork of the repository on GitHub.

2. **Create a Pull Request:**

    - Open a pull request from your forked repository to the main repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Thanks to the Django and MindsDB communities for their invaluable documentation and support.
- Special appreciation to the open-source contributors whose libraries and tools made this project possible.
- Gratitude to the developers of PostgreSQL for providing a reliable and robust database solution.
- Inspired by various online tutorials and articles that provided insights on supply chain optimization and machine learning integration.

---

Feel free to customize this `README.md` file according to your project's specific details and requirements.
