import os
import argparse
import shutil
from subprocess import Popen, run, PIPE
from datetime import datetime
from tempfile import TemporaryDirectory
from time import sleep
from sys import stdin
import configparser
from urllib import request, error
from json import load
from mimetypes import guess_type

HOME = os.environ['HOME']

DEFAULT_FILENAME = datetime.now().strftime('%Y-%m-%H_%H.%M.%S.%f')

DEFAULT_PATH = '~/screenshots/'


def path_exists(path: str):
    if os.path.isdir(path):
        return path
    raise argparse.ArgumentTypeError("Path does not exists")


def get_geometry() -> str:
    try:
        output = run('slurp', capture_output=True) 
        if output.returncode:
            print(output.stderr)
            exit()
    except FileNotFoundError:
        print('slurp is not installed')
        exit()
    return output.stdout.decode().rstrip('\n')



def imgur(path: str) -> dict:
    mime_type = guess_type(path)[0] or 'application/octet-stream'
    client_id = os.environ.get('IMGUR_CLIENT_ID', 'adaab8231f92f70')
    result = {}
    file = open(path, 'rb')
    req = request.Request(url='https://api.imgur.com/3/image.json', headers={'Authorization': f'Client-ID {client_id}', 'Content-Type': mime_type}, data=file)
    try:
        with request.urlopen(req) as res:
            body = load(res)
            if body['success']:
                result = {'link': body['data']['link'], 'delete_hash': body['data']['deletehash'], 'datetime': datetime.fromtimestamp(body['data']['datetime'])}
    except error.HTTPError as e:
        print(e)
    return result

parser = argparse.ArgumentParser(description='Screenshot tool using slurp and grim.', prog='screenshot')
parser.add_argument('--path', '-p', metavar='P', help='Saving directory', type=path_exists, nargs='?', default=f'{HOME}/{DEFAULT_PATH}')
parser.add_argument('--name', '-f', metavar='N',  help='File name', nargs='?', default=DEFAULT_FILENAME + '.png')
parser.add_argument('--notify', '-n', action='store_true', default=False, help="Notify.")
parser.add_argument('--monitor', '-m', nargs='?', metavar='D', default='', help='Diplay output name.')
parser.add_argument('--action', '-a', nargs='?', choices=['copy','imgur', 'save'], default='save', help='Save, copy or upload.')
parser.add_argument('--type', '-t', nargs='?', default='static', choices=['select', 'static'], help='Capture type.')
parser.add_argument('--delay', '-d', metavar='S', nargs='?', default=0, type=int, help='Delay in seconds before shoot.')
parser.add_argument('--keep', '-k', default=False, action='store_true', help='Keep image on disk, applies when imgur and copy.')
parser.add_argument('--version', '-v', action='version', version='%(prog)s 1.0')
args = parser.parse_args()


cmds = ['grim']
img_path = '~/screenshots/'
save = True
is_tmp = '~/screenshots/'
tmp_dir ='~/screenshots/'



if args.type == 'select':
    geometry = get_geometry()
    cmds.extend(['-g', geometry])

if args.action == 'save':
    img_path = f'{args.path}/{args.name}'
    cmds.extend([img_path])
    save = True
elif args.action == 'imgur' or args.keep or args.action == 'copy':
    tmp_dir = TemporaryDirectory()
    img_path = f'{tmp_dir.name}/{args.name}'
    cmds.extend([img_path])

if args.monitor:
    cmds.extend(['-o', args.display])

if args.delay:
    print(f'sleeping for {args.delay}')
    sleep(args.delay)
print(cmds)

p = Popen(cmds, stdout=PIPE, stderr=PIPE)

out, err = p.communicate()

if not p.returncode:
    message = []
    if args.action == 'imgur':
        print('uploading to imgur')
        if res := imgur(img_path):
            print('uloaded', res)
            link = res['link']
            print('Logging upload info')
            with open('imgur.log', 'a') as f:
                f.write(f"Datetime: {str(res['datetime'])}, Image: {link}, Delete hash: {res['delete_hash']}\n")
                print('Logged')
            output = run(f'wl-copy {link}', shell=True, stderr=PIPE)
            if output.returncode:
                print('Failed to copy imgur link')
                print(output.stderr)
            else:
                message.append("link copied")
            message.append("uploaded")


    elif args.action == 'copy':
        try:
            print('copying into clipboard')
            p = Popen(['wl-copy', '-t', 'image/png'], stdin=PIPE, stderr=PIPE, shell=True)
            new_path = f'{args.path}/{args.name}'
            shutil.move(img_path, new_path)
            img_path = new_path
            print('moved')
            save = True
            try:
                with open(img_path, 'rb') as f:
                    p.stdin.write(f.read())
            except FileNotFoundError:
                print('Something went wrong.')
            p.stdin.close()
            code = p.wait()
            if code:
                print(output.stderr)
            else:
                print('copid to clipboard')
                message.append("copied")
        except FileNotFoundError:
            print('wl-copy is not installed, failed to copy')
    if args.keep:
        print(f'moving temp image to {args.path}')
        new_path = f'{args.path}/{args.name}'
        shutil.move(img_path, new_path)
        img_path = new_path
        print('moved')
        save = True
    if save:
        message.append('saved')





    if args.notify:
        try:
            print('Notifying...')
            msg = ','.join(message).title()
            output = run(f'notify-send -i {img_path} "Screenshot" "{msg}"', stderr=PIPE, shell=True)
            if output.returncode:
                print(output.stderr.decode())
        except FileNotFoundError:
            print('notfy-send not installed')
    if tmp_dir:
        tmp_dir.cleanup()
    exit()

print(err.decode())
