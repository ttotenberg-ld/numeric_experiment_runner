from utils.api_handler import checkRateLimit as api_call


'''
Makes an API call to LaunchDarkly to get the list of variations for the inputted FLAG_KEY
'''
def variation_list(projectkey, flagkey, apikey):
    flag_api_url = f'/flags/{projectkey}/{flagkey}'
    response = api_call("GET", flag_api_url, apikey, {}).json()
    variation_list = response['variations']
    number_of_variations = len(variation_list)
    variation_list = []

    for i in range(number_of_variations):
        variation_list.append(response['variations'][i]['value'])

    return variation_list