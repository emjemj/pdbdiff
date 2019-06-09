import argparse
import requests


class PeeringDBDiff:

    def __init__(self, first_asn, second_asn):
        self.first = self.__fetch(first_asn)
        self.second = self.__fetch(second_asn)
        self.first_asn = first_asn
        self.second_asn = second_asn

        self.first_fac_ids = set([x['fac_id'] for x in
                                 self.first['netfac_set']])
        self.second_fac_ids = set([x['fac_id'] for x in
                                  self.second['netfac_set']])
        self.first_ixlan_ids = set([x['ixlan_id'] for x in
                                   self.first['netixlan_set']])
        self.second_ixlan_ids = set([x['ixlan_id'] for x in
                                    self.second['netixlan_set']])

    def first_unique_facilities(self) -> list:
        return self.__unique(entries=self.first['netfac_set'],
                             first_keys=self.first_fac_ids,
                             second_keys=self.second_fac_ids,
                             set_key='netfac_set',
                             key='fac_id')

    def second_unique_facilities(self) -> list:
        return self.__unique(entries=self.second['netfac_set'],
                             first_keys=self.second_fac_ids,
                             second_keys=self.first_fac_ids,
                             set_key='netfac_set',
                             key='fac_id')

    def common_facilities(self) -> list:
        return self.__common(entries=self.first['netfac_set'],
                             first_keys=self.first_fac_ids,
                             second_keys=self.second_fac_ids,
                             set_key='netfac_set',
                             key='fac_id')

    def first_unique_ixes(self) -> list:
        return self.__unique(entries=self.first['netixlan_set'],
                             first_keys=self.first_ixlan_ids,
                             second_keys=self.second_ixlan_ids,
                             set_key='netixlan_set',
                             key='ixlan_id')

    def second_unique_ixes(self) -> list:
        return self.__unique(entries=self.second['netixlan_set'],
                             first_keys=self.second_ixlan_ids,
                             second_keys=self.first_ixlan_ids,
                             set_key='netixlan_set',
                             key='ixlan_id')

    def common_ixes(self) -> list:
        return self.__common(entries=self.first['netixlan_set'],
                             first_keys=self.first_ixlan_ids,
                             second_keys=self.second_ixlan_ids,
                             set_key='netixlan_set',
                             key='ixlan_id')

    def __unique(self, entries: list, set_key: str, key: str, first_keys: list,
                 second_keys: list) -> list:
        values = first_keys - second_keys

        return self.__find(entries=entries,
                           set_key=set_key,
                           key=key,
                           values=values)

    def __common(self, entries: list, set_key: str, key: str, first_keys: list,
                 second_keys: list) -> list:
        values = first_keys.intersection(second_keys)

        return self.__find(entries=entries,
                           set_key=set_key,
                           key=key,
                           values=values)

    def __find(self, entries: list, set_key: str, key: str,
               values: list) -> list:
        return [x for x in entries if x[key] in values]

    def __fetch(self, asn: int) -> dict:
        r = requests.get('https://peeringdb.com/api/net?depth=2&asn={}'.
                         format(asn))
        return r.json()['data'][0]


parser = argparse.ArgumentParser('Compare two peeringdb entries')
parser.add_argument('--common', '-c',
                    help='display common entities (default is unique)',
                    action='store_true')
parser.add_argument('--ix', '-i', help='Display exchanges',
                    action='store_true')
parser.add_argument('--facility', '-f', help='Display facilities',
                    action='store_true')
parser.add_argument('--first', '-1', help='Only display entries for first asn',
                    action='store_true')
parser.add_argument('--second', '-2',
                    help='Only display entries for second asn',
                    action='store_true')
parser.add_argument('asn', metavar='ASN', type=int, nargs=2)
args = parser.parse_args()

first = args.asn[0]
second = args.asn[1]

diff = PeeringDBDiff(first, second)

if args.common:
    if args.ix or (not args.ix and not args.facility):
        print('Common exchanges')
        print('Name')
        print('-' * 89)
        for ix in diff.common_ixes():
            print('{}'.format(ix['name']))
        print('\n')

    if args.facility or (not args.ix and not args.facility):
        print('Common facilities')
        print('{name:60} {city:20} {country:5}'.format(name='Name',
                                                       city='City',
                                                       country='Country'))
        print('-' * 89)
        for fac in diff.common_facilities():
            print('{name:60} {city:20} {country:5}'.format(
                                                   name=fac['name'][0:60],
                                                   city=fac['city'],
                                                   country=fac['country']))
        print('\n')
else:
    if args.ix or (not args.ix and not args.facility):
        if args.first or (not args.first and not args.second):
            print('Unique exchanges for AS{}'.format(first))
            print('Name')
            print('-' * 89)
            for ix in diff.first_unique_ixes():
                print('{}'.format(ix['name']))
            print('\n')

        if args.second or (not args.first and not args.second):
            print('Unique exchanges for AS{}'.format(second))
            print('Name')
            print('-' * 89)
            for ix in diff.second_unique_ixes():
                print('{}'.format(ix['name']))
            print('\n')

    if args.facility or (not args.ix and not args.facility):
        if args.first or (not args.first and not args.second):
            print('Unique facilities for AS{}'.format(first))
            print('{name:60} {city:20} {country:5}'.format(name='Name',
                                                           city='City',
                                                           country='Country'))
            print('-' * 89)
            for fac in diff.first_unique_facilities():
                print('{name:60} {city:20} {country:5}'.format(
                      name=fac['name'][0:60], city=fac['city'],
                      country=fac['country']))
            print('\n')

        if args.second or (not args.first and not args.second):
            print('Unique facilities for AS{}'.format(second))
            print('{name:60} {city:20} {country:5}'.format(name='Name',
                                                           city='City',
                                                           country='Country'))
            print('-' * 89)
            for fac in diff.second_unique_facilities():
                print('{name:60} {city:20} {country:5}'.format(
                      name=fac['name'][0:60], city=fac['city'],
                      country=fac['country']))
            print('\n')
