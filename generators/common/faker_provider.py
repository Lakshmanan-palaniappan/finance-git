"""
Shared Faker Instance
"""

import random

from faker import Faker

fake = Faker("en_IN")

Faker.seed(100)

random.seed(100)