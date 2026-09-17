#!/usr/bin/env bash
# Check the live tag setup from a network that DNS-blocks Google.
# The office resolver returns 0.0.0.0 for googletagmanager.com, so we resolve
# over DNS-over-HTTPS and pin the IP with --resolve.
set -euo pipefail
GTM_ID="${1:-GTM-MNHMB7C9}"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

IP=$(curl -s -H "accept: application/dns-json" \
  "https://cloudflare-dns.com/dns-query?name=www.googletagmanager.com&type=A" \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['Answer'][0]['data'])")
echo "resolved www.googletagmanager.com -> $IP (via DoH)"

echo
echo "== is the GTM snippet on the live page? =="
curl -s -L --compressed -A "$UA" -H "Sec-Fetch-Dest: document" -H "Sec-Fetch-Mode: navigate" \
  https://amamiitalia.com/ | grep -oE "GTM-[A-Z0-9]+|G-[A-Z0-9]{8,}" | sort | uniq -c

echo
echo "== what does the published container actually contain? =="
curl -s --compressed --resolve "www.googletagmanager.com:443:$IP" -A "$UA" \
  -H "Referer: https://amamiitalia.com/" \
  "https://www.googletagmanager.com/gtm.js?id=$GTM_ID" \
| python3 -c "
import re,sys,json
t=sys.stdin.read()
m=re.search(r'var data = (\{.*?\});\s*\n', t, re.S)
if not m: print('  could not parse container'); sys.exit(1)
r=json.loads(m.group(1))['resource']
for k in ('macros','tags','predicates','rules'):
    print(f'  {k+\":\":11} {len(r.get(k,[]))}')
if not r.get('tags'):
    print('  >> CONTAINER IS EMPTY - it loads but fires nothing.')
    print('     Import analytics/GTM-MNHMB7C9-container-import.json, then Submit > Publish.')
"
