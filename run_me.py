# Import custom libs
import _csv_to_json
import _config
import _ipf_api
import _send_email

# Import built-in libs
from pprint import pprint



def normalize_ipf_output(input_dict):

    output_dict = {}

    for entry in input_dict:
        # normalise hostname
        # strip domain name
        hostname = entry['hostname'].lower()
        hostname = hostname.split('.')[0]
        hostname = hostname.split('/')[0]

        if hostname not in output_dict:
            output_dict[hostname] = {}
            output_dict[hostname][entry['intName'].lower()]=entry['cost']
        else:
            output_dict[hostname][entry['intName'].lower()]=entry['cost']

    return output_dict



def cost_diff(csv_in,ipf_in):
    
    output_dict = {}

    for device in csv_in:

        # add device to output_dict if not there
        if device not in output_dict:
            output_dict[device] = {}

        # iterate throught interfaces in csv_in and extract the expected
        # (csv) and known (ipf) OSPF costs
        for interface in csv_in[device]:
            csv_cost = csv_in[device][interface]
            ipf_cost = ipf_in[device][interface]


            # check if costs are the same or different and mark accordingly
            if csv_cost == ipf_cost:
                output_dict[device][interface] = {
                    'ipf_cost'   : ipf_cost,
                    'csv_cost'   : csv_cost,
                    'match'      : True
                    }
            else:
                output_dict[device][interface] = {
                    'ipf_cost'   : ipf_cost,
                    'csv_cost'   : csv_cost,
                    'match'      : False
                    }

    return output_dict

    

def email_body_gen(input_dict):

    body = []

    # for each failed check on the input dict, create a single line of test and add to a list
    for device in input_dict:
        for interface in input_dict[device]:
            if input_dict[device][interface]['match'] == False:
                expected = str(input_dict[device][interface]['csv_cost'])
                actual   = str(input_dict[device][interface]['ipf_cost'])
                body.append('Device: ' + device + ' | Interface: ' + interface + ' | Expected Cost: ' + expected + ' | Actual Cost: ' + actual)

    #join each list object into a single string with line breaks
    body = "\n".join(body)

    return body



def main():

    # Extract data from input file to dict
    """
    Dict Structure:

    base_interface_costs {
        'device_name' : {
            'interface':'cost',
            'interface':'cost'
            },
        'device_name' : {
            'interface':'cost',
            'interface':'cost'
            }
        }
    """

    base_interface_costs = _csv_to_json.make(input_csv)


    # Get auth tokens
    accessToken, tokenHeaders = _ipf_api.api_auth(ipf_user, ipf_pass, ipf_base_url)


    # Get interface OSPF costs from latest snapshit
    devicesPayload = {"columns":["hostname","intName","cost",],"snapshot":snapshotId,}
    devicesEndpoint = ipf_base_url + 'tables/routing/protocols/ospf/interfaces'
    
    ipf_output_full = _ipf_api.api_post(devicesEndpoint, tokenHeaders, devicesPayload).json()['data']


    # normalise IPF output to match base_interface_cost dict structure
    ipf_output = normalize_ipf_output (ipf_output_full)


    # compare cost difference
    cost_comparison = cost_diff(base_interface_costs, ipf_output)

    # generate email body
    email_body = email_body_gen(cost_comparison)

    # send email
    email_subject = 'IPFabric - OSPF Cost Baseline'
    _send_email.send(email_sender, email_target, email_server, email_subject, email_body)




if __name__ == '__main__':

    #Load global variables
    input_csv = _config.input_file
    
    ipf_user = _config.ipf_creds['username']
    ipf_pass = _config.ipf_creds['password']

    ipf_base_url = 'https://' + _config.ipf_server + '/api/v1/'

    email_server = _config.email['server']
    email_sender = _config.email['sender']
    email_target = _config.email['target']

    snapshotId = '$last'

    main()
