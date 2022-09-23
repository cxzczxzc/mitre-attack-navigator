from sheet_controller import SheetController
from layer_generator import LayerGenerator

#key_path
key_path = "/Users/saadx/Documents/PSO/2022/dnb/mitre-attack/mitre-attack-navigator/key.json"

#spreadsheet variables
spreadsheet_id = "1fE8bIMZ5-uymBmPeYlt70vvn-DcCVrYZDuIza7Lpwrs"
services_spreadsheet_range = "'Assessment by Control/Product'!A1:F50"
control_to_technique_range = "'Control/Product to Technique'!A1:J441"

#MITRE ATT&CK Layer Variables
layer_source_file_path = "/Users/saadx/Documents/PSO/2022/dnb/mitre-attack/mitre-attack-navigator/layer.json"
capability_layer_destination_path = "/Users/saadx/Documents/PSO/2022/dnb/mitre-attack/mitre-attack-navigator/capability_matrix.json"
capability_layer_name = "DnB Capability Matrix - Current State"
configuration_layer_name = "DnB Configuration Matrix - Current State"
configuration_layer_destination_path = "/Users/saadx/Documents/PSO/2022/dnb/mitre-attack/mitre-attack-navigator/configuration_matrix.json"
future_state_layer_name =  "DnB MITRE Matrix - Future State"
future_state_layer_destination_path = "/Users/saadx/Documents/PSO/2022/dnb/mitre-attack/mitre-attack-navigator/future_state.json"

#sheets connection
sheet_controller = SheetController(key_path=key_path)
technique_to_capability = sheet_controller.get_technique_to_capability_map(spreadsheet_id=spreadsheet_id, range=control_to_technique_range)
technique_to_configuration = sheet_controller.get_technique_to_configuration_map(spreadsheet_id=spreadsheet_id, range=control_to_technique_range)
technique_to_future_state = sheet_controller.get_technique_to_future_configuration_map(spreadsheet_id=spreadsheet_id, range=control_to_technique_range)

#layer generation

layer_generator = LayerGenerator(layer_source_file_path=layer_source_file_path, 
                                output_file_path=capability_layer_destination_path)
layer_generator.generate_layer(technique_map=technique_to_capability,
                                name=capability_layer_name)


layer_generator = LayerGenerator(layer_source_file_path=layer_source_file_path, 
                                output_file_path=configuration_layer_destination_path)
layer_generator.generate_layer(technique_map=technique_to_configuration,
                                name=configuration_layer_name)


layer_generator = LayerGenerator(layer_source_file_path=layer_source_file_path, 
                                    output_file_path=future_state_layer_destination_path)
layer_generator.generate_layer(technique_map=technique_to_future_state, 
                                name=future_state_layer_name)


