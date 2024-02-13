import json

json_text = '{ "firstName": "tester", "lastName": "tester", "city": "Vilnius" }'
s = json.loads(json_text)

print(s)

s['firstName'] = "Bidas"
s['lastName'] = "Vareikis"
s['age'] = 2002
s['wingspan'] = 200

print(s)