from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class TechniqueMap():
    def __init__(self, technique=None, capability=None, color=None, service=None, notes=None, enabled=True):
        self.technique = technique
        self.capability = capability
        self.color =  color
        self.service = service
        self.enabled = enabled
        self.notes = notes

class SheetController():
    def __init__(self, key_path):
        self.key_path = key_path
        self.blue_color = "#4285F4"
        self.green_color = "#34A653"
        self.red_color = "#EA4335"
        self.yellow_color = "#FBBC04"

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
        notes_row_index = 9
        
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
                    technique_to_capability.color = self.green_color #green
                elif row[capability_row_index].strip()=='N':
                    technique_to_capability.color = self.red_color #red
                elif row[capability_row_index].strip()=='TBD':
                    technique_to_capability.color = self.yellow_color #yellow
                elif row[capability_row_index].strip()=='3rd Party Tool In Use':
                    technique_to_capability.color = self.blue_color #blue
                if len(row) >= notes_row_index:
                    if row[notes_row_index].strip():
                        technique_to_capability.notes = row[notes_row_index].strip()
                else:
                    if technique_to_capability.color == self.green_color:
                        technique_to_capability.notes = "Capability in place"
                    elif technique_to_capability.color == self.blue_color:
                        technique_to_capability.notes = "Using third party product"
                    elif technique_to_capability.notes == self.yellow_color:
                        technique_to_capability.notes = "Capability planned but not available yet"
                    elif technique_to_capability.notes == self.red_color:
                        technique_to_capability.notes == "Gap because relevant GCP service is not in use"
                result.append(technique_to_capability)
        return result
    
    def get_technique_to_configuration_map(self, spreadsheet_id, range):
            rows = self.get_values(spreadsheet_id=spreadsheet_id, range_name=range)
            
            service_row_index = 0
            technique_row_index = 1
            configuration_row_index = 7
            service_row_index = 0
            notes_row_index = 10
            
            result = []
            for row in rows:
                if row[technique_row_index].strip() == "N/A - Not Mappable" or \
                row[technique_row_index].strip() == "Technique ID":
                    continue
                else:
                    technique_to_capability = TechniqueMap()
                    technique_to_capability.technique = row[technique_row_index].strip()
                    technique_to_capability.capability = row[configuration_row_index].strip()
                    technique_to_capability.service = row[service_row_index].strip()
                    if row[configuration_row_index].strip()=='Y':
                        technique_to_capability.color = "#34A653" #green
                    elif row[configuration_row_index].strip()=='N':
                        technique_to_capability.color = "#EA4335" #red
                    elif row[configuration_row_index].strip()=='TBD':
                        technique_to_capability.color = "#FBBC04" #yellow
                    elif row[configuration_row_index].strip()=='3rd Party Service in Use':
                        technique_to_capability.color = "#4285F4" #blue
                    else:
                        technique_to_capability.color = "#EA4335" #red
                    result.append(technique_to_capability)
            return result

