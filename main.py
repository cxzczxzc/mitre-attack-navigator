from sheet_controller import SheetController

sheet_controller = SheetController(key_path="/Users/saadx/Documents/PSO/2022/dnb/mitre-attack/mitre-attack-navigator/key.json")
spreadsheet_id = "1fE8bIMZ5-uymBmPeYlt70vvn-DcCVrYZDuIza7Lpwrs"
services_spreadsheet_range = "'Assessment by Control/Product'!A1:F50"
control_to_technique_range = "'Control/Product to Technique'!A1:J441"
unused_services = sheet_controller.get_unused_services(spreadsheet_id=spreadsheet_id, range=services_spreadsheet_range)
technique_to_capability = sheet_controller.get_technique_to_capability_map(spreadsheet_id=spreadsheet_id, range=control_to_technique_range)
sheet_controller.disable_unsused_services(unused_services, technique_to_capability)

