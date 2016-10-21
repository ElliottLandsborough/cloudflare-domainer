#!/bin/bash

# config
cloudflare_key=""
cloudflare_zone_id=""
cloudflare_record_id=""
cloudflare_email=""
domain=""

# get my ip
ip=$(wget https://wtfismyip.com/text -q -O -);

# set the ip
curl -X PUT "https://api.cloudflare.com/client/v4/zones/$cloudflare_zone_id/dns_records/$cloudflare_record_id" \
     -H "X-Auth-Email: $cloudflare_email" \
     -H "X-Auth-Key: $cloudflare_key" \
     -H "Content-Type: application/json" \
     --data "{\"type\":\"A\",\"name\":\"$domain\",\"content\":\"$ip\"}";