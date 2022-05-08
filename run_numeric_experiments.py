from dotenv import load_dotenv #pip install python-dotenv
import ldclient
from ldclient.config import Config
import os
import random
import time
from utils.get_variation_list import variation_list
from utils.create_user import random_ld_user


'''
Get environment variables
'''
load_dotenv()

SDK_KEY = os.environ.get('SDK_KEY')
API_KEY = os.environ.get('API_KEY')
PROJECT_KEY = os.environ.get('PROJECT_KEY')
FLAG_KEY = os.environ.get('FLAG_KEY')
METRIC_NAME = os.environ.get('METRIC_NAME')
NUMBER_OF_ITERATIONS = os.environ.get('NUMBER_OF_ITERATIONS')


'''
Initialize the LaunchDarkly SDK
'''
ldclient.set_config(Config(SDK_KEY))


'''
Make an API call to LaunchDarkly to get the list of variations for the desired flag.
'''
flag_variations = variation_list(PROJECT_KEY, FLAG_KEY, API_KEY)


'''
Get user input for the center numeric value
'''
def get_center_value(variation):
    center_value = input(f"Please enter a center value for {variation}: ")
    return center_value

'''
Get user input for the numeric spread
'''
def get_spread_value(variation):
    spread = input(f"Please enter a spread for {variation}: ")
    return spread


'''
Constructs a dictionary of variations and their numeric values
center = that variations center. This will end up being the average metric value for that variation
spread = the spread above and below the center. Will randomize metric values between the low and high spread values
'''
def construct_variations_dictionary():
    num_variations = len(flag_variations)
    variations_dict_list = []
    numeric_list = []

    for i in range(num_variations):
        variations_dict_list.append(f'{flag_variations[i]}_center')
        variations_dict_list.append(f'{flag_variations[i]}_spread')
        numeric_list.append(f'{get_center_value(flag_variations[i])}')
        numeric_list.append(f'{get_spread_value(flag_variations[i])}')
    
    variations_dictionary = dict(zip(variations_dict_list, numeric_list))
    return variations_dictionary

variations_dictionary = construct_variations_dictionary()


'''
Calculates the numeric value to return as part of the numeric experiment. Takes two arguments:
center = variation_center. This should be the overall average of the numeric experiment you want to see
spread = variation_spread. This spread is used to calculate how high above and below the center value the returned values can be.
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
        flag_variation = str(ldclient.get().variation(FLAG_KEY, random_user, False))
        center = variations_dictionary[f'{flag_variation}_center']
        spread = variations_dictionary[f'{flag_variation}_spread']

        metric_value = numeric_value(center, spread)

        ldclient.get().track(METRIC_NAME, random_user, None, metric_value)
        print(f"Executing {str(flag_variation)}: {str(i+1)}/{NUMBER_OF_ITERATIONS}")
        print(f"Metric value: {str(metric_value)}")



'''
Execute!
'''
callLD()


'''
Responsibly close the LD Client
'''
ldclient.get().close()