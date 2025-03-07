import azure.functions as func
import datetime
import json
import logging
import os

app = func.FunctionApp()

@app.route(route="HttpTriggerWithAuthen", auth_level=func.AuthLevel.FUNCTION)
def HttpTriggerWithAuthen(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    # Retrieve function key from environment variables
    stored_function_key = os.getenv('FUNCTION_KEY')
    print (stored_function_key)
    if not stored_function_key:
        logging.error("Stored function key not found.")
        return func.HttpResponse(
            "Internal server error: Function key not configured.",
            status_code=500
        )

    # Get the function key from request headers
    provided_key = req.headers.get('x-functions-key')

    # Check for the function key
    if not provided_key or provided_key != stored_function_key:
        logging.warning("Missing or invalid function key.")
        return func.HttpResponse(
            "Unauthorized request. A valid function key is required.",
            status_code=401
        )
    
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )