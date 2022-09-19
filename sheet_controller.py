class SheetController():
    def __init__(self):
        pass

# 1. Get data from the sheet
# 2. From the "Assessment by Control/Product", get all the services where the service is not in use
# by the customer. The techniques that use this service will be greyed out in
# the attack matrix
# 3. From the "Control/Product to Technique", get the capabilites (Column G) for each technique (Column B).
# 4. From the "Control/Product to Technique", get the configuration (Column H) for each technique (Column B).
# 5. Parse the stuff and generate a JSON layer file 
#   Parsing logic:
#   
