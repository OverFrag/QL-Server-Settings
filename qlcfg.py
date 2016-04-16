import os
import argparse
import urllib.request
import urllib.error
import json
import base64
import collections


REPOSITORY = 'https://api.github.com/repos/OverFrag/QL-Server-Settings'
ACCESS_FILE = 'baseq3/access.txt'
WORKSHOP_FILE = 'baseq3/workshop.txt'


def update_access(files, allow_remove):
    remote = get_remote_file(ACCESS_FILE)

    for file in files:
        print('Processing file: %s' % file)

        current = collections.OrderedDict({})

        linenum = 1

        f = open(os.path.expanduser(file), 'a+')
        f.seek(0)

        for line in f:
            if not line.startswith('#') and not line.startswith(';'):
                steamid, access = map(str.strip, line.split('|'))
                current[steamid.strip()] = {'access': access.strip(), 'linenum': linenum}

            linenum += 1

        for line in remote:
            if line.startswith(';ex'):
                line = line[3:].split(';')
                steamid, access = map(str.strip, line[0].split('|'))
                name = line[1]

                if steamid in current:
                    if allow_remove:
                        del current[steamid]
                    else:
                        print('\tSteamID "%s" (name: %s) is marked as removed. Consider updating access.txt to remove it [line %i]' % (steamid, name, current[steamid]['linenum']))

            elif not line.startswith('#') and not line.startswith(';'):
                line = line.split(';')
                steamid, access = map(str.strip, line[0].split('|'))
                name = line[1]

                if steamid in current:
                    if current[steamid]['access'] != access:
                        if allow_remove:
                            print('\tSteamID "%s" (name: %s) changes access level from '
                                  '%s to %s' % (
                                    steamid,
                                    name,
                                    current[steamid]['access'],
                                    access
                                  ))
                            current[steamid] = {'access': access}
                        else:
                            print('\tSteamID "%s" (name: %s) is marked to change access from %s to %s. '
                                  'Consider updating access.txt [line %i]' % (
                                    steamid,
                                    name,
                                    current[steamid]['access'],
                                    access,
                                    current[steamid]['linenum']
                                  ))
                else:
                    print('\tAdding SteamID "%s" (name: %s) as %s' % (steamid, name, access))
                    current[steamid] = {'access': access}

        write = []

        for steamid in current:
            write.append('%s|%s' % (steamid, current[steamid]['access']))

        f.seek(0)
        f.truncate()
        f.write('\n'.join(write))
        f.close()


def update_workshop(files):
    remote = get_remote_file(WORKSHOP_FILE)

    for file in files:
        print('Processing file: %s' % file)

        current = []

        f = open(os.path.expanduser(file), 'a+')
        f.seek(0)

        for line in f:
            if not line.startswith('#') and not line.startswith(';'):
                current.append(line.strip())

        for line in remote:
            if not line.startswith('#') and not line.startswith(';'):
                itemid, name = map(str.strip, line.split(';'))

                if itemid not in current:
                    print('\tAdding Workshop item "%s" (name: %s)' % (itemid, name))
                    current.append(itemid)

        f.seek(0)
        f.truncate()
        f.write('\n'.join(current))
        f.close()


def get_remote_file(file):
    try:
        response = urllib.request.urlopen('/'.join([REPOSITORY, 'contents', file]))

        json_ = json.loads(response.read().decode('utf-8'))
        data = base64.b64decode(json_['content'])

        return data.decode('utf-8').splitlines()
    except urllib.error.HTTPError as e:
        print('[ERROR] Could not connect to settings repository (code: %s)' % e.code)
        exit(1)
    except urllib.error.ContentTooShortError:
        print('[ERROR] There was a problem with downloading the data. Try again later')
        exit(1)
    except urllib.error.URLError:
        print('[ERROR] There was an unknown error. PM admins at http://discord.overfrag.com/')
        exit(1)


def main():
    parser = argparse.ArgumentParser(description='OverFrag\'s Quake Live Settings Manager',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--access',
                        dest='access',
                        nargs='*',
                        help='Update defined access files',
                        metavar='FILE'
                        )

    parser.add_argument('--remove',
                        dest='remove',
                        help='Allows script to remove access ids marked as removed',
                        action='store_true')

    parser.add_argument('--workshop',
                        dest='workshop',
                        nargs='*',
                        help='Update defined workshop files',
                        metavar='FILE'
                        )

    args = parser.parse_args()

    if args.access is not None:
        update_access(args.access, args.remove)

    if args.workshop is not None:
        update_workshop(args.workshop)

if __name__ == '__main__':
    main()
