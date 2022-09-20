from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class TechniqueMap():
    def __init__(self, technique=None, capability=None, color=None, service=None, enabled=True):
        self.technique = technique
        self.capability = capability
        self.color =  color
        self.service = service
        self.enabled = enabled





# 1. Get data from the sheet
# 2. From the "Assessment by Control/Product", get all the services where the service is not in use
# by the customer. The techniques that use this service will be greyed out in
# the attack matrix
# 3. From the "Control/Product to Technique", get the capabilites (Column G) for each technique (Column B).
# 4. From the "Control/Product to Technique", get the configuration (Column H) for each technique (Column B).
# 5. Parse the stuff and generate a JSON layer file 
#   Parsing logic:
#   


class SheetController():
    def __init__(self, key_path):
        self.key_path = key_path

    def get_values(self, spreadsheet_id, range_name):
        creds, _ = google.auth.load_credentials_from_file(self.key_path)
        try:
            service = build('sheets', 'v4', credentials=creds)

            result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id, range=range_name).execute()
            rows = result.get('values', [])
            print(f"{len(rows)} rows retrieved")
            return rows
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error



    def get_unused_services(self, spreadsheet_id, range):
        rows = self.get_values(spreadsheet_id=spreadsheet_id, range_name=range)
        capability_row_index = 4
        service_row_index = 0
        i = 1 
        unused_services = []
        for row in rows:
            if row[capability_row_index] == 'N':
                unused_service = ''.join([i for i in row[service_row_index] if not i.isdigit()])
                unused_service = unused_service.replace('.','')
                unused_service = unused_service.lstrip()
                unused_services.append(unused_service)
        return unused_services
            
        

    def get_technique_to_capability_map(self, spreadsheet_id, range):
        rows = self.get_values(spreadsheet_id=spreadsheet_id, range_name=range)
        service_row_index = 0
        technique_row_index = 1
        capability_row_index = 6
        service_row_index = 0
        result = []
        for row in rows:
            if row[technique_row_index].strip() == "N/A - Not Mappable" or \
            row[technique_row_index].strip() == "Technique ID":
                continue
            else:
                technique_to_capability = TechniqueMap()
                technique_to_capability.technique = row[technique_row_index].strip()
                technique_to_capability.capability = row[capability_row_index].strip()
                technique_to_capability.service = row[service_row_index].strip()
                if row[capability_row_index].strip()=='Y':
                    technique_to_capability.color = "#34A653" #green
                elif row[capability_row_index].strip()=='N':
                    technique_to_capability.color = "#EA4335" #red
                elif row[capability_row_index].strip()=='TBD':
                    technique_to_capability.color = "#FBBC04" #yellow
                elif row[capability_row_index].strip()=='3rd Party Service in Use':
                    technique_to_capability.color = "#4285F4" #blue
                else:
                    technique_to_capability.color = "#EA4335" #red
                result.append(technique_to_capability)
        return result

    def disable_unsused_services(self, unused_services, technique_map):
        for data in technique_map:
            if data.service is not None:
                if data.service in unused_services:
                    print(f"The service {data.service} for technique {data.technique} is disabled")
                    data.enabled = False

