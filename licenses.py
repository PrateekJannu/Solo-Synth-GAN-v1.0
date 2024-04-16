import json


# Path to your CycloneDX SBOM file
sbom_file_path = 'ssgan.bom'


with open(sbom_file_path, 'rb') as sbom_file:
    bom = json.load(sbom_file)


#print(bom)
# Extract license information
licenses=set()
for y in bom['components']:
    if "licenses" in y.keys():
        if 'license' in y['licenses'][0].keys():
            if 'id' in y["licenses"][0]["license"].keys():
                licenses.add(y["licenses"][0]["license"]["id"])
            #licenses.add(y["licenses"]["license"]["name"])
            elif 'name' in y["licenses"][0]["license"].keys():
                licenses.add(y["licenses"][0]["license"]["name"])



#lol=[[licenses.add(x['license']['text']) for x in y['licenses']] ]
for i,lic in enumerate(licenses):
    print('\n License No',i,'and Name is',lic)