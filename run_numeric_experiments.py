from dotenv import load_dotenv #pip install python-dotenv
import ldclient
from ldclient.config import Config
import names
import os
import random
import time
import uuid
from utils.user_countries import random_country


'''
Get environment variables
'''
load_dotenv()

SDK_KEY = os.environ.get('SDK_KEY')
FLAG_NAME = os.environ.get('FLAG_NAME')
METRIC_NAME = os.environ.get('METRIC_NAME')
TRUE_CENTER_VALUE = os.environ.get('TRUE_CENTER_VALUE')
TRUE_SPREAD = os.environ.get('TRUE_SPREAD')
FALSE_CENTER_VALUE = os.environ.get('FALSE_CENTER_VALUE')
FALSE_SPREAD = os.environ.get('FALSE_SPREAD')
NUMBER_OF_ITERATIONS = os.environ.get('NUMBER_OF_ITERATIONS')


'''
Initialize the LaunchDarkly SDK
'''
ldclient.set_config(Config(SDK_KEY))


'''
Construct and return a random user
'''
def random_ld_user():
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    plan = random.choice(["free", "silver", "gold"])
    email = first_name + "." + last_name + random.choice(["@gmail.com", "@yahoo.com", "@hotmail.com"])

    user = {
        "key": str(uuid.uuid4()),
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "country": random_country(),
        "custom": {
          "plan": plan
        }
    }
    return user


'''
Calculates the numeric value to return as part of the numeric experiment. Takes two arguments:
center = [VARIATION]_CENTER_VALUE. This should be the overall average of the numeric experiment you want to see
spread = [VARIATION]_SPREAD. This spread is used to calculate how high above and below the center value the returned values can be.
'''
def numeric_value(center, spread):
    low = int(center) - int(spread)
    high = int(center) + int(spread)
    value = random.randint(low, high)
    return value


'''
Evaluate the flags for randomly generated users, and make the track() calls to LaunchDarkly
'''
def callLD():
    for i in range(int(NUMBER_OF_ITERATIONS)):

        random_user = random_ld_user()
        flag_variation = ldclient.get().variation(FLAG_NAME, random_user, False)

        if flag_variation:
            metric_value = numeric_value(TRUE_CENTER_VALUE, TRUE_SPREAD)
            ldclient.get().track(METRIC_NAME, random_user, None, metric_value)
            print("Executing " + str(flag_variation) + ": " + str(i+1) + "/" + NUMBER_OF_ITERATIONS)
            print("Metric value: " + str(metric_value))
                

        else:
            metric_value = numeric_value(FALSE_CENTER_VALUE, FALSE_SPREAD)
            ldclient.get().track(METRIC_NAME, random_user, None, metric_value)
            print("Executing " + str(flag_variation) + ": " + str(i+1) + "/" + NUMBER_OF_ITERATIONS)
            print("Metric value: " + str(metric_value))


'''
Execute!
'''
callLD()


'''
Responsibly close the LD Client
'''
ldclient.get().close()