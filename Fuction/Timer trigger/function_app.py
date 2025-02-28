import datetime
import logging
import azure.functions as func

app = func.FunctionApp()

@app.function_name(name="mytimer")
@app.timer_trigger(schedule="0 */1 * * * *", 
              arg_name="mytimer",
              run_on_startup=True) 
def test_function(mytimer: func.TimerRequest) -> None:
    #format to utc time 
    #utc_timestamp = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
    #if mytimer.past_due:
    #    logging.info('The timer is past due!')
    #logging.info('Python timer trigger function ran at %s', utc_timestamp)
    # using local timestame
    local_timestamp = datetime.datetime.now().isoformat()
    if mytimer.past_due:
        logging.info('The timer is past due!')
    logging.info('Python timer trigger function ran at %s', local_timestamp)