import logging  
import azure.functions as func  
def main(req: func.HttpRequest) -> func.HttpResponse:  
         logging.info('Processing request for GoogleAuthen.')  
         return func.HttpResponse("Hello from GoogleAuthen!", status_code=200)