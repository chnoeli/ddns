import requests
import json

f = open('creds.json')
creds = json.load(f)

# Get current public ip
response = requests.get("https://api.ipify.org?format=json")
currentPublicIp = response.json()['ip']
godaddyBaseURL = "https://api.godaddy.com/"

# get current DNS record settings
headers = {'Authorization': 'sso-key ' + creds['key'] + ':' + creds['secret']}
response = requests.get(godaddyBaseURL + "v1/domains/" +
                        creds['domain']+"/records/A/" + creds['cn'], headers=headers)
godaddyIP = response.json()[0]['data']

print("Godaddy IP: " + godaddyIP + " Current Public IP: " + currentPublicIp)
#  eck if dns record is already equal
if currentPublicIp != godaddyIP:
    print("Public IP is different updating DNS Record")
    uri = godaddyBaseURL + "v1/domains/" + \
        creds['domain']+"/records/A/"+creds['cn']
    body = [
        {
            "data": currentPublicIp,
            "name": creds['cn'],
            "ttl": 600,
            "type": "A"
        }
    ]
    # update dns record
    response = requests.put(uri, headers=headers, json=body)

    uri = godaddyBaseURL + "v1/domains/" + \
        creds['domain']+"/records/A/"+creds['cn']
    response = requests.get(uri, headers=headers)
    if response.json()[0]['data'] == currentPublicIp:
        print("Successfuly updated DNS Record")
    else:
        print("Somthing went wrong while updating the dns record")

elif currentPublicIp == godaddyIP:
    print("Public Ip and Godaddy IP are the same no changes")
else:
    print("We have some problem please hold on.")
