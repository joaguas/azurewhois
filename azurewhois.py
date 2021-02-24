import argparse
import json
import pandas as pd
import re
import requests
import sys
from ipaddress import ip_network, IPv4Address


def engine(ip):
    try:
        ip = IPv4Address(ip)
    except Exception as e:
        print(' Make you use a valid IPv4 Address: %s' % e, file=sys.stderr)
        sys.exit(1)
    latest = getlatest()
    df = jsontodf(latest)
    whois(df, ip)


def jsontodf(latest):
    url = 'https://download.microsoft.com/download/7/1/D/' \
          '71D86715-5596-4529-9B13-DA13A5DE5B63/' \
          'ServiceTags_Public_{0}.json'.format(latest)
    try:
        data = pd.read_json(url)
        try:
            data = pd.json_normalize(data['values'])
            df = data[["name", "properties.addressPrefixes"]]
            df = df.rename(columns={"name": "service",
                                    "properties.addressPrefixes": "prefix"})
            df = df.explode('prefix', ignore_index=True)
            df = df[~df.prefix.str.contains("::")]
            df = df.reset_index(drop=True)
            df = df.drop_duplicates(subset=['prefix'], keep='first')
            idx = df['prefix'].str.split(
                    '/', expand=True).sort_values(
                            [1, 0], ascending=False).index
            df = df.reindex(idx).reset_index(drop=True)
        except ValueError:
            print("This is not the json file you are looking for... Exiting")
            return
    except Exception as e:
        print("Unable to access %s:  %s " % (url, e), file=sys.stderr)
        sys.exit(1)
    return df


def getlatest():
    try:
        html_content = requests.get(
                'https://www.microsoft.com/en-us/download/'
                'details.aspx?id=56519'
                ).content.decode('utf-8')
        date = re.search('_(\\d+)\\.json', html_content).group(1)
    except Exception:
        print('Could not find the latest Service Tags update...'
              'Will try an older known version (2021-02-15).')
        date = '20210215'
    return date


def whois(df, ip):
    for index, entry in df.iterrows():
        if ip in ip_network(entry['prefix']):
            print('IP address %s is associated with Service Tag '
                  '%s (within the %s range)' % (ip, entry['service'],
                                                entry['prefix']))
            sys.exit(0)
    print('IP address %s was not found on Azure IP Ranges and '
          'Service Tags – Public Cloud' % ip)
    sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: azurewhois <IPv4>', file=sys.stderr)
        sys.exit(1)
    else:
        engine(sys.argv[1])
