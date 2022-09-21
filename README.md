# MITRE ATT&CK Analysis and Heatmap Toolkit for GCP
A suite for generating MITRE ATT&amp;CK Navigation Layers from Google Sheets

### Purpose
This suite is used for performing a risk assessment for a GCP organization using the MITRE ATT&CK Matrix. This matrix helps understand security in the context of a threat actor's pathways into an organization. 

#### TTPs
TTP is an acronym for Tactics, Techniques, and Procedures.

- **Tactics**: Tactics refer to the art or skill of employing available means to accomplish an end. Tactics convey what an attacker is doing, without delving into the technical details. For example: Initial Access.
- **Techniques**: Techniques refer to the unique ways or methods used to perform missions, functions, or tasks. Techniques are non-prescriptive, there is no defined order of execution with techniques. For example: T1407 - Valid Accounts is a technique that applies across various tactics like Inital Access and Privilege Escalation.
- **Procedures**: Procedures refer to standard, detailed steps that prescribe how to perform specific tasks. These are unique to each threat actor, and can be used to fingerprint attacker's movement through a system. For example: An attacker might consistently perform a single `ping -n 1` to the target system prior to executing an attack. The single instance of this command is an indicator, and multiple indicators form a pattern, which is called a procedure. 

*Reference: [On TTPs](http://ryanstillions.blogspot.com/2014/04/on-ttps.html)*

## Artifacts

There are two main artifacts involved:
- A Google Sheets Document
    - This spreadsheets contains **3 tabs** that map out various aspects of the attack matrix. 

        1. **Assessment by Control/Product:** This tab contains a list of all the GCP services relevant within the context of the attack matrix. To protect, detect, or respond to a TTP, the relevant GCP services should be in use by the customer, and configured properly. This sheet is a good starting point to understand which services are in use by a customer. 
        2. **Control/Product to Technique:** This tab contains a list of Techniques mapped to the GCP service that can protect, detect, or respond against each technique. Just because a customer has a GCP service enabled, it does mean that they're secured against a technique. The service has to be configured properly as well.This sheet maps techniques to services (Capability) as well as proper setup of those services (Capabilities)
        3. **Tactic/Technique**: This tab contains an overall view of TTPs and GCP services.
- A set of python scripts

    - These scripts parse the data contained in Google Sheets into JSON
    - The JSON is then uploaded to render heatmaps on the [MITRE ATT&CK® Navigator website.](https://mitre-attack.github.io/attack-navigator/)
    - The official GCP MITRE ATT&CK® Navigator heatmap can be seen [here](https://mitre-attack.github.io/attack-navigator/#layerURL=https://center-for-threat-informed-defense.github.io/security-stack-mappings/GCP/layers/platform.json)


 ## Usage
 Assuming you have a Google Sheets Document with all the tabs already filled out, you can run this code to generate the heatmap
 ### Prerequisites
 1. pip version 22.1.2
 2. Python 3.8.9
 3. A GCP service account key, with Google Sheets API enabled, and access to the the Google Sheets Document (Share the document with the service account email ID)
 
 ### Generate the heatmap
 - Run `git clone https://github.com/cxzczxzc/mitre-attack-navigator.git` from a terminal
 - Download the GCP Service Account key with Google Sheets API enabled and save it in the `mitre-attack-navigator` folder
 - Modify the variables in `main.py` to match the values in your case. (Lines 5-17) 
 - Run `init.sh` to install the python packages
 - Run `python .\main.py` to generate the heatmap

 ### Visualize the heatmap
 - TBD

