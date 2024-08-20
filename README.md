# DeepChecks Backend Developer Assignment
This project is a FastAPI application for handling interactions and alerts. It includes endpoints for creating interactions, uploading CSV files to create multiple interactions, and retrieving alerts.

## Features
- **Log LLM Interactions**: Store input-output pairs of LLM interactions in a database.
- **Calculate Metrics**: Calculate metrics (e.g., length of input/output) on each interaction and store the results.
- **Alerts**: Trigger alerts based on specific conditions:
  - Metric value exceeds a threshold.
  - Metric value is an outlier compared to the rest of the values.
- **Upload Interactions via CSV**: Upload a CSV file of interactions, which are processed in the background.

## Project Structure
```
deepchecks/
├── app/
│   ├── controllers/
│   ├── utils/
│   └── services/
├── core/
│   └── models/
├── infrastructure/
│   ├── database.py
│   └── repositories/
├── tests/
│   └── test_app.py
├── main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Installation
After installing this application, Make sure to create a .env file and copy the content of the .env.example into your 
newly created file. Also, ensure that you've assigned values to all the variables present. For example, 
the `ALERT_THRESHOLD` variable.

### Using Docker Compose
1. Ensure docker-compose.yml is in the root of your project directory.
2. Build and start the services:
    ```
    BUILDKIT_PROGRESS=plain docker-compose up --build
    ```
 The application will be available at http://127.0.0.1:8000.

### Without Docker
1. Clone the repository:
    ```
    git clone https://github.com/BryanAdamson/deepchecks.git
    cd deepchecks
    ```
2. Create a virtual environment and activate it:
    ```
    python -m venv env
    source env/bin/activate
    ```
3. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```
4. Start the FastAPI application:
    ```
    uvicorn main:app --reload
    ```
The application will be available at http://127.0.0.1:8000. The API documentation will be available at http://127.0.0.1:8000/docs.

## Tests
To run the tests, use:
    ```
    pytest
    ```

## Endpoints
When testing the endpoints with curl, make sure to set the content-type as `application/json`.

### Interactions
- #### POST api/interactions/bulk<br>
  Accepts a CSV file containing interactions data, processes each row to calculate metrics, stores them in the database, and creates alerts based on predefined conditions.
  #### Request Body:
    ```
    Form-data with a single file field named `file` containing the CSV file.
    ```
  #### Response:
    ```
    {
      "success": true,
      "data": null,
      "message": "CSV file received. Processing in the background..."
    }
    ```
  
- #### POST api/interactions<br>
  Creates a new interaction and calculates the metrics.<br>
  #### Request Body:
    ```
    {
      "input_text": "string",
      "output_text": "string"
    }
    ```
  #### Response:
    ```
    {
      "success": true, 
      "data": {
        "output": "string", 
        "created_at": "2024-07-19T12:46:57.170331", 
        "id": 1, 
        "input": "string"
      }, 
      "message": "Interaction created successfully"
    }
    ```
  
### Alerts
- #### GET api/alerts<br>
  Gets all the alerts in the system.<br>
 
  #### Response:
    ```
    {
        "success": true,
        "data": [
            {
                "alert_type": "threshold",
                "interaction_id": 2,
                "element": "input",
                "id": 1,
                "metric_value": 258.0,
                "created_at": "2024-07-19T12:57:37.888120"
            }
        ],
        "message: "Alerts fetched successfully"
    }
    ```
- #### GET api/alerts?interaction_id=2<br>
  Gets all the alerts for a specific interaction.<br>
 
  #### Response:
    ```
    {
        "success": true,
        "data": [
            {
                "alert_type": "threshold",
                "interaction_id": 1,
                "element": "input",
                "id": 1,
                "metric_value": 254.0,
                "created_at": "2024-07-10T12:57:37.888120"
            }
        ],
        "message: "Alerts fetched successfully"
    }
    ```
