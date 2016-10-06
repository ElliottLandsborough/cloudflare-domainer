import sys
import json
from pprint import pprint # same as print_r e.g pprint(var)
# python 2 only
import urllib2 as urllib
from urllib2 import urlopen
from urllib2 import Request

def getConfig():
    try:
        with open('config.json') as data_file:    
            data = json.load(data_file)
            return data;
    except IOError:
        sys.exit('config.json does not exist') 
    except ValueError:
        sys.exit('config.json is invalid') 

CFG = getConfig()

def getIpAddress():
    try:
        body = urlopen(str(CFG['wtfismyip_api'])).read().decode('utf8') # get url
        data = json.loads(body) # parse json...
        return str(data['YourFuckingIPAddress'])
    except urllib.HTTPError as e:
        error_message = e.read()
        sys.exit('Something went wrong with ' + CFG['wtfismyip_api'] + ': ' + error_message)
    except ValueError:
        sys.exit(CFG['wtfismyip_api'] + ' is invalid json') 


def setCloudFlareIp():
    ip = getIpAddress();
    post_fields = {'type':'A', 'name':CFG['domain'], 'content':ip}
    url = "https://api.cloudflare.com/client/v4/zones/" + CFG['cloudflare_zone_id'] + '/dns_records/' + CFG['cloudflare_record_id']
    request = Request(url, json.dumps(post_fields))
    request.add_header('X-Auth-Email', CFG['cloudflare_email'])
    request.add_header('X-Auth-Key', CFG['cloudflare_key'])
    request.add_header('Content-Type', 'application/json')
    request.get_method = lambda: 'PUT'
    try:
        response = urlopen(request)
        print(CFG['domain'] + ': ' + ip)
    except urllib.HTTPError as e:
        error_message = e.read()
        sys.exit('Cloudflare error: ' + error_message)

setCloudFlareIp()