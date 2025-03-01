
import re
import os
import requests
import argparse
import concurrent.futures


parser = argparse.ArgumentParser()
parser.add_argument('-s', help='hash', dest='hash')
parser.add_argument('-f', help='file containing hashes', dest='file')
parser.add_argument('-d', help='directory containing hashes', dest='dir')
parser.add_argument('-t', help='number of threads', dest='threads', type=int)
args = parser.parse_args()


end = '\033[0m'
red = '\033[91m'
green = '\033[92m'
white = '\033[97m'
dgreen = '\033[32m'
yellow = '\033[93m'
back = '\033[7;91m'
run = '\033[97m[~]\033[0m'
que = '\033[94m[?]\033[0m'
bad = '\033[91m[-]\033[0m'
info = '\033[93m[!]\033[0m'
good = '\033[92m[+]\033[0m'


cwd = os.getcwd()
directory = args.dir
file = args.file
thread_count = args.threads or 4
result = []
notFound = []



def alpha(hashvalue, hashtype):
    return False


def beta(hashvalue, hashtype):
    response = requests.get(
        'http://hashtoolkit.com/reverse-hash/?hash=' + hashvalue).text
    match = re.search(r'/generate-hash/?text=.*?"', response)
    if match:
        return match.group(1)
    else:
        return False


def gamma(hashvalue, hashtype):
    response = requests.get(
        'http://www.nitrxgen.net/md5db/' + hashvalue, verify=False).text
    if response:
        return response
    else:
        return False


def delta(hashvalue, hashtype):
    # data = {'auth':'8272hgt', 'hash':hashvalue, 'string':'','Submit':'Submit'}
    # response = requests.post('http://hashcrack.com/index.php' , data).text
    # match = re.search(r'<span class=hervorheb2>(.*?)</span></div></TD>', response)
    # if match:
    #    return match.group(1)
    # else:
    return False


def theta(hashvalue, hashtype):
    response = requests.get(
        'http://md5decrypt.net/Api/api.php?hash=%s&hash_type=%s&email=deanna_abshire@proxymail.eu&code=1152464b80a61728' % (hashvalue, hashtype)).text
    if len(response) != 0:
        return response
    else:
        return False
    
def threaded(hashvalue):
    resp = crack(hashvalue[1][0]) 
    detail = []  
    if resp:        
        detail = [hashvalue[0][0],hashvalue[1][0],resp]
        result.append(detail)
    else:
        detail = [hashvalue[0][0],hashvalue[1][0]]
        notFound.append(detail)

    



def crack(hashvalue):
    result = False
    if len(hashvalue) == 32:
        if not file:
            print ('%s Hash function : MD5' % info)
        for api in md5:
            r = api(hashvalue, 'md5')
            if r:
                return r
    elif len(hashvalue) == 40:
        if not file:
            print ('%s Hash function : SHA1' % info)
        for api in sha1:
            r = api(hashvalue, 'sha1')
            if r:
                return r
    elif len(hashvalue) == 64:
        if not file:
            print ('%s Hash function : SHA-256' % info)
        for api in sha256:
            r = api(hashvalue, 'sha256')
            if r:
                return r
    elif len(hashvalue) == 96:
        if not file:
            print ('%s Hash function : SHA-384' % info)
        for api in sha384:
            r = api(hashvalue, 'sha384')
            if r:
                return r
    elif len(hashvalue) == 128:
        if not file:
            print ('%s Hash function : SHA-512' % info)
        for api in sha512:
            r = api(hashvalue, 'sha512')
            if r:
                return r
    else:
        if not file:
            print ('%s This hash type is not supported.' % bad)
            quit()
        else:
            return False

md5 =  [gamma, alpha, beta, theta, delta]
sha1 = [alpha, beta, theta, delta]
sha256 = [alpha, beta, theta]
sha384 = [alpha, beta, theta]
sha512 = [alpha, beta, theta]

def miner(file):
    lines = []
    found = []
    with open(file, 'r') as f:
        for line in f:
            lines.append(line.strip('\n'))

    matches = []
    for line in lines:    
        email = re.findall(r'[\w.-]+@[\w.-]+', line)
        password_hash = re.findall(r'[a-f0-9]{128}|[a-f0-9]{96}|[a-f0-9]{64}|[a-f0-9]{40}|[a-f0-9]{32}', line)
        details = [email,password_hash]
        matches.append(details)
        if matches:
            found = matches

    print ('%s Hashes found: %i' % (info, len(found)))
    threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=thread_count)
    futures = (threadpool.submit(threaded, hashvalue) for hashvalue in found)
    for i, _ in enumerate(concurrent.futures.as_completed(futures)):
        if i + 1 == len(found) or (i + 1) % thread_count == 0:
            print('%s Progress: %i/%i' % (info, i + 1, len(found)), end='\r')


if file:
    try:
        miner(file)
    except KeyboardInterrupt:
        pass
    with open('cracked.txt', 'w+') as f:
         for detail in result :
             print(detail)
             f.write(detail[0] + ' : ' + detail[1] + ' : ' + detail[2] + '\n' )
             print('sad')
    with open('Notfound.txt', 'w+') as f:
         for detail in notFound :
             print(detail)
             f.write(detail[0] + ' : ' + detail[1] + '\n' )
             print('sad')

    print ('%s Results saved in cracked-%s' % (info, file.split('/')[-1]))