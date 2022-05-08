import time
import requests
from requests.exceptions import HTTPError
# pip install requests


BASE_URL = "https://app.launchdarkly.com/api/v2"
CALL_THRESHOLD = 1 # If the API call limit falls below this number, the calls will pause and retry once the limit is reset.


class RateLimitError(Exception):
    '''Exception used by the main function when the rate limit is too low'''
    pass


def timeToNextReset(nextReset):
    '''
    Compares current time to the rate limit reset time. Then sees how many whole seconds left until the reset, and returns that number
    '''
    currentMilliTime = round(time.time() * 1000)
    if nextReset - currentMilliTime > 0:
        return round((nextReset - currentMilliTime) // 1000)
    else:
        return 0


def checkRateLimit(method, url, apikey, body):
    '''
    Main function of this wrapper. Sends the call with the following arguments:
    
    :param method: "GET", "POST", "PATCH", "DELETE"
    :param url: Everything after the BASE_URL
    :param apikey: Your LaunchDarkly API Key
    :param body: The body of the request. This can be blank - as {}.

    This will make your call, and check the rate limit. If the current rate limit is below the CALL_THRESHOLD, 
    it will retry three times before throwing an error and giving up.
    '''

    defaultTries = 5
    # defaultTries is the base number of retries this wrapper should perform. After that, it will raise a RateLimitError. Set it to whatever integer you deem appropriate.
    tries = defaultTries
    delay = 5

    def getResetTime():
        '''
        Finds the next rate limit reset time, and sleeps until that time.
        '''
        resetTime = int(response.headers['X-Ratelimit-Reset'])

        nonlocal delay
        delay = timeToNextReset(resetTime)
        if delay < 1:
            delay = .5
            # Setting a delay floor of .5 seconds helps with time rounding on the limit reset comparison.

        nonlocal tries
        tries -= 1

        print('Rate limit is too low. It is currently ' + str(rateLimitRemaining) + '. Retrying in ' + str(delay) + ' seconds.')
        time.sleep(delay)

    while tries > 0:

        try:
            response = requests.request(method, BASE_URL + url, headers = {'Authorization': apikey, 'Content-Type': 'application/json'}, data = body)
            rateLimitRemaining = response.headers['X-Ratelimit-Route-Remaining']

        except HTTPError as http_err:
            print('An HTTP error occurred: ' + str(http_err))
            break
        except Exception as err:
            print('An error occurred: ' + str(err))
            break


        if int(rateLimitRemaining) <= CALL_THRESHOLD:
            getResetTime()
            if tries == 0:
                raise RateLimitError
        else:
            tries = defaultTries
            return response
