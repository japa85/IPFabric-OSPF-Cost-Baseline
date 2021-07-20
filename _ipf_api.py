import requests,sys

# Suppressing SSL certificate warnings if needed
requests.packages.urllib3.disable_warnings()

def api_auth(username, password, base_url):
    authEndpoint = base_url + 'auth/login'
    authData = { 'username': username, 'password' : password }
        
    # Initiating authentication request to obtain authentication token
    authPost = requests.post(authEndpoint, json=authData, verify=False)
    if not authPost.ok:
        print('Unable to authenticate: ' + authPost.text)
        sys.exit()
    # Collecting the accessToken 
    accessToken = authPost.json()['accessToken']
    # Creating the tokenHeaders 
    tokenHeaders = { 'Authorization' : 'Bearer ' + accessToken}
    return accessToken, tokenHeaders


def api_post(devicesEndpoint, tokenHeaders, devicesPayload):
    # Contacting the API endpoint for device inventory
    reqDevices = requests.post(devicesEndpoint, headers=tokenHeaders, json=devicesPayload, verify=False)
    if not reqDevices.ok:
        print('Unable to authenticate: ' + reqDevices.text)
        sys.exit()
    return reqDevices
