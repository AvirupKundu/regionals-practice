import random

def generate_random_data(structure):
    """
    Recursively generates random data for a given JSON structure.
    """
    if isinstance(structure, dict):
        return {k: generate_random_data(v) for k, v in structure.items()}
    elif isinstance(structure, list):
        # For lists, we'll assume we want a list of random values for each item
        return [generate_random_value(item) for item in structure]
    else:
        return generate_random_value(structure)

def generate_random_value(param_name):
    """
    Generates a random value based on the parameter name.
    This is a simplified and extendable way to generate relevant data.
    """
    param_name = param_name.lower()
    if "current" in param_name:
        return round(random.uniform(0, 1000), 2)
    if "voltage" in param_name:
        return round(random.uniform(220, 400), 2)
    if "temperature" in param_name:
        return round(random.uniform(20, 90), 2)
    if "pressure" in param_name:
        return round(random.uniform(1, 10), 2)
    if "resistance" in param_name:
        return round(random.uniform(0, 1000), 2)
    if "time" in param_name or "duration" in param_name:
        return round(random.uniform(0, 1000), 2)
    if "power" in param_name:
        return round(random.uniform(0, 10000), 2)
    if "frequency" in param_name:
        return round(random.uniform(49.8, 50.2), 2)
    if "status" in param_name or "flag" in param_name or "alarm" in param_name:
        return random.choice([0, 1])
    if "count" in param_name:
        return random.randint(0, 1000)
    if "id" in param_name:
        return ''.join(random.choices('0123456789ABCDEF', k=10))
    if "date" in param_name or "timestamp" in param_name:
        return random.randint(1672531200, 1704067199) # Random timestamp in 2023
    # Default for other numeric-like sounding names
    if any(x in param_name for x in ["value", "level", "factor", "index", "capacity"]):
        return round(random.uniform(0, 100), 2)

    # Default for anything else, return a random string
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8))