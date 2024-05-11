import json
import re
dataMap = {
    "['Initial Access']" : 1,
    "['Execution']" : 2,
    "['Persistence']" : 3,
    "['Privilege Escalation']" : 4,
    "['Defense Evasion']" : 5,
    "['Credential Access']" : 6,
    "['Discovery']" : 7,
    "['Lateral Movement']" : 8,
    "['Collection']" : 9,
    "['Command and Control']" : 10,
    "['Exfiltration']" : 11,
    "['Impact']" : 12
}
def mitre_mapping(rulenames):
    def process(rulenames):
            with open('./mitre.json', 'r') as f:
                dataS = json.loads(f.read())
                print(type(dataS))
            
            for rule in rulenames:
                mapping = dataS.get(str(rule))
                if mapping != None:
                    mapping_final = mapping.get('mapping')

                    part = r"^{'(.*?)'"

                    xong = re.findall(part, str(mapping_final))
                    return dataMap[str(xong)]     
                else:
                    pass
    result_map = process(rulenames) 
    if result_map != None:
        return result_map
    else:
        return 9    
    
#print(mitre_mapping(['quangdv', 'Excessive Database Connections']))