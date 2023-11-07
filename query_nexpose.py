# pylint: disable=missing-docstring


import argparse
import json

from typing import Optional, Union
from requests import Session, Response
from requests.auth import HTTPBasicAuth


# pylint: disable=too-many-arguments,too-many-locals, broad-except
def main(
        domain: str,
        username: str,
        password: str,
        proxies: Optional[dict] = None,
        hostname: Optional[str] = None,
        list_tags: bool = False,
) -> Union[None, str, list, dict]:
    session = Session()

    headers: dict = {
        'Accept': 'application/json',
        'Content-Type': 'application/json; Charset=UTF-8',
    }
    session.headers = headers
    session.auth = HTTPBasicAuth(username, password)

    asset_id: Optional[str] = None
    asset: Optional[dict] = None

    # search for host
    try:
        query_filter: dict = {
            'field': 'host-name',
            'operator': 'is',
            'value': hostname,
        }
        body_params: dict = {
            'filters': [
                query_filter,
            ],
            'match': 'all',
        }
        resp_query: Response = session.post(
            url=f'https://{domain}/api/3/assets/search',
            json=body_params,
            headers=headers,
            proxies=proxies,
        )
        resp_query.raise_for_status()
        data_query: dict = resp_query.json()
        resources: list = data_query.get('resources')
        for resource in resources:
            asset = resource
        asset_id = asset.get('id')
    except Exception as exc_query:
        print(f'{exc_query}')

    # query for tags
    if list_tags:
        try:
            resp_entity: Response = session.get(
                url=f'https://{domain}/api/3/assets/{asset_id}/tags',
                headers=headers,
                proxies=proxies,
            )
            resp_entity.raise_for_status()
            data_entity: dict = resp_entity.json()
            resources: list = data_entity.get('resources')
            asset['tags'] = resources
        except Exception as exc_entity:
            print(f'{exc_entity}')

    return asset


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--domain',
        type=str,
        required=True,
        help="The FQDN/IP for your InsightVM host (not full URL)",
    )
    parser.add_argument(
        '--username',
        default=None,
        type=str,
        required=True,
        help='The username to authenticate with',
    )
    parser.add_argument(
        '--password',
        default=None,
        type=str,
        required=True,
        help='The password for the username',
    )
    parser.add_argument(
        '--hostname',
        default=None,
        type=str,
        required=False,
        help='The hostname to query for',
    )
    parser.add_argument(
        '--proxies',
        type=str,
        required=False,
        help="JSON structure specifying 'http' and 'https' proxy URLs",
    )
    parser.add_argument(
        '--list-tags',
        action='store_true',
        default=False,
        required=False,
        help="Get tags for the specified host",
        dest='list_tags',
    )

    args = parser.parse_args()

    proxies: Optional[dict] = None
    if proxies:
        try:
            proxies: dict = json.loads(args.proxies)
        except Exception as exc_json:
            print(f'WARNING: failure parsing proxies: {exc_json}: proxies provided: {proxies}')

    result = main(
        domain=args.domain,
        username=args.username,
        password=args.password,
        proxies=proxies,
        list_tags=args.list_tags,
    )

    if result:
        if args.list_tags:
            tags: list = result.get('tags')
            if tags and isinstance(tags, list):
                print(f'tags count: {len(tags)}')
        print(json.dumps(result, indent=4))
    else:
        print('No results found')
