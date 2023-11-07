# query_nexpose

test query for InsightVM API v3:<br>
* look up a single host by hostname `--hostname HOST`
* look up asset by hostname with tags`--hostname HOST --list-tags`

# usage
```
$ python main.py --help
usage: query_nexpose.py [-h] --domain DOMAIN --username USERNAME --password PASSWORD [--hostname HOSTNAME] [--proxies PROXIES] [--list-tags]

options:
  -h, --help                     show this help message and exit
  --domain DOMAIN                The FQDN/IP for your InsightVM server (not full URL)
  --username USERNAME            The username to authenticate with
  --password PASSWORD            The password for the username
  --hostname HOSTNAME            The hostname to query for
  --proxies PROXIES              JSON structure specifying 'http' and 'https' proxy URLs
  --list-tags                    Get tags for the specified host
```


# example: look up host with vulnerability details
`python3 query_nexpose.py --domain my.nexpose.domain.tld --username blah --password blah --hostname abc123 --list-tags`
