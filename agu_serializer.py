from pyingest.serializers.classic import Tagged
import json

f = open('agu_final_data.json')
json_file = json.load(f)

outputfp = open('agu_tagged.tag', 'a')

for record in json_file:
    # print(document)
    serializer = Tagged()
    serializer.write(record, outputfp)

outputfp.close()
