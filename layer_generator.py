import json
from turtle import color
from sheet_controller import TechniqueMap

class LayerGenerator():

    def __init__(self, layer_source_file_path, output_file_path):
        self.layer_source_file_path = layer_source_file_path
        self.output_file_path = output_file_path
        self.blue_color = "#4285F4"
        self.green_color = "#34A653"
        self.red_color = "#EA4335"
        self.yellow_color = "#FBBC04"
    
    def get_legend_items(self):
        return [ {
            "color": "#34A653",
            "label": "Capability in place"
        },
        {
            "color": "#EA4335",
            "label": "Capability not in place (gap)"
        },
        {
            "color": "#4285F4",
            "label": "Using third party product"
        },
        {
            "color": "#FBBC04",
            "label": "Capability planned but not available"
        },
    ]
    def generate_layer(self, technique_map, name):
        data = []
        disabled_techniques = self.get_techniques_not_relevant_to_GCP()
        with open(self.layer_source_file_path, 'r') as f:
            data = json.load(f)
            data["name"] = name
            data["legendItems"] = self.get_legend_items()
            
            for detail in data["techniques"]:
                if detail["techniqueID"] in disabled_techniques:
                    detail["enabled"] = False
                    continue
                map_items = self.find_item_in_map(technique_map, detail["techniqueID"])
                #set correct color
                if len(map_items) == 0:
                    print("Technique "+ str(detail["techniqueID"]) + " not found")
                elif len(map_items) == 1:
                    detail["color"] = map_items[0].color
                elif len(map_items) > 1:
                    detail["color"] = self.calculate_technique_color(map_items)
                    if detail["color"] == self.blue_color:
                        print("Blue:"+detail["techniqueID"])
                #set custom metadata
                metadata = self.calculate_metadata(map_items=map_items, metadata=detail["metadata"])
                detail["metadata"] = metadata
            with open(self.output_file_path, 'w') as result:
                json.dump(data, result)
    # in cases when a technique has multiple controls and applies to multiple tactics
    # at various levels of protection, detection, and response, a calculation is done for the matrix
    # the score is indicated by a color - red, blue, yellow, or green
    def calculate_technique_color(self, map_items):
        colormap = {self.blue_color :0,
        self.green_color : 0,
        self.red_color: 0,
        self.yellow_color :0}
        for item in map_items:
            if item.color == self.blue_color:
                colormap[self.blue_color] = colormap[self.blue_color] + 1
            elif item.color == self.yellow_color:
                colormap[self.yellow_color] = colormap[self.yellow_color] + 1
            elif item.color == self.red_color:
                colormap[self.red_color] = colormap[self.red_color] + 1
            elif item.color == self.green_color:
                colormap[self.green_color] = colormap[self.green_color] + 1
        if colormap[self.blue_color] > 0:
            if colormap[self.blue_color] > colormap[self.yellow_color]:
                return self.blue_color
            else:
                return self.yellow_color
        return str(max(colormap, key=lambda key: colormap[key]))
        

    def calculate_metadata(self, map_items, metadata):
        notes_string = str(len(map_items)) +" GCP services apply" + str(len(map_items))
        service_status = []
        for item in map_items:
            if item.notes is None:
                item.notes = ""
            if item.color == self.red_color:
                service_status.append({item.service: "This service is not in use at DnB."})
            if item.color == self.blue_color:
                service_status.append({item.service: "A third party tool is in use." + item.notes })
            if item.color == self.green_color:
                service_status.append({item.service: "Capability is available." + item.notes})
            if item.color == self.yellow_color:
                service_status.append({item.service: "Capability is planned but not active yet." +item.notes})
        
        notes = [{"name" : "Notes", "value": notes_string}, {"divider":True}]
        final_metadata = []
        final_metadata.append(notes)

        if metadata is not None:
            for x in service_status:
                pass
        return final_metadata


            
        
                



            


    
    def find_item_in_map(self, technique_map, techniqueID):
        items = []
        for item in technique_map:
            if item.technique == techniqueID:
                items.append(item)
        return items
    def get_techniques_not_relevant_to_GCP(self):
        return ["T1592",
                "T1589",
                "T1591",
                "T1597",
                "T1596",
                "T1593",
                "T1594",
                "T1583",
                "T1586",
                "T1587",
                "T1585",
                "T1608",
                "T1200",
                "T1091",
                "T1559",
                "T1129",
                "T1047",
                "T1197",
                "T1176",
                "T1140",
                "T1006",
                "T1480",
                "T1599",
                "T1620",
                "T1207",
                "T1216",
                "T1535",
                "T1220",
                "T1606",
                "T1558",
                "T1539",
                "T1111",
                "T1010",
                "T1217",
                "T1526",
                "T1482",
                "T1083",
                "T1615",
                "T1201",
                "T1120",
                "T1012",
                "T1518",
                "T1614",
                "T1007",
                "T1124",
                "T1534",
                "T1563",
                "T1091",
                "T1080",
                "T1123",
                "T1119",
                "T1185",
                "T1115",
                "T1005",
                "T1039",
                "T1025",
                "T1074",
                "T1113",
                "T1125",
                "T1092",
                "T1001",
                "T1568",
                "T1573",
                "T1102",
                "T1030",
                "T1029",
                "T1531",
                "T1489",
                "T1529", 
                "T1565"]
    
