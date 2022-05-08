import names
import random
from utils.user_countries import random_country
import uuid


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