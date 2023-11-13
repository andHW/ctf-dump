"""
Usage: py fake_ground_offer.py > out
"""

import sys
import re
import requests
import time
from bs4 import BeautifulSoup
import concurrent.futures
from math import sin, floor
from collections import defaultdict


SITE = "http://chal-b.hkcert23.pwnable.hk:28137"


def gacha1(s: requests.Session):
    r = s.get(SITE, params={"gacha1": ""})
    return r


def gacha10(s: requests.Session):
    r = s.get(SITE, params={"gacha10": ""})
    return r


def parseGachaResponse(r: requests.Response):
    soup = BeautifulSoup(r.text, "html.parser")
    session_id_text = soup.select("p")[0].text
    session_id = session_id_text.rsplit(" ")[-1]
    inventory_text = soup.select("p")[2].text
    card_info_list = inventory_text.split("\n")[2:7]

    inventory = defaultdict(int)
    for card_level_info in card_info_list:
        levelMatch = re.search(r"\[([A-Z]*)\]", card_level_info)
        level = levelMatch.group(1)
        amt = int(card_level_info.rsplit()[-1])
        inventory[level] = amt

    can_sell_acc = inventory["UR"] + inventory["SSR"] >= 20

    got = []
    got_text = soup.select_one("h2").text
    got = got_text.replace("You got ", "").split(",")

    got_dict = defaultdict(int)
    for card in got:
        card = card.strip()
        if card not in got_dict:
            got_dict[card] = 1
        else:
            got_dict[card] += 1

    return session_id, inventory, can_sell_acc, got_dict


"""
Get 29 gachas by sending: gacha10 + gacha1 * 9 + gacha10
"""


def summonCards():
    s = requests.Session()

    r = gacha10(s)

    # # send get requests in parallel
    # with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
    #     fs = [executor.submit(s.get, SITE, params={"gacha1": ""}) for i in range(9)]
    #     for future in concurrent.futures.as_completed(fs):
    #         future.result()

    for i in range(9):
        gacha1(s)

    r = gacha10(s)
    return parseGachaResponse(r)


"""
seed's range: [1, 3600)
n's range: 1 or 10
"""


def php_gacha_simulation(n, seed):
    out = []
    for i in range(1, n + 1):
        x = sin(i * seed)
        r = x - floor(x)
        out.append(r)
    return out


"""
Result:
[1 1 1 1 1 1 1 1 1 1] appears at following seeds: 710, 1420, 2130, 2840, 3550
they are all multiples of 710.
"""


def gacha10_sim():
    for seed in range(1, 3600):
        res = php_gacha_simulation(10, seed)
        res = ["1" if f <= 0.004 else "0" for f in res]
        print(f"{seed:04}: {' '.join(res)}")


"""
Failed.
"""


def brute_force():
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        fs = [executor.submit(summonCards) for seed in range(1)]
        for future in concurrent.futures.as_completed(fs):
            res = future.result()
            print(*res)
            session_id, _, can_sell_acc = res
            if can_sell_acc:
                print(f"YESSSSSS: {session_id}")
                break


def has_n_ur_or_ssr(n, cards_dict):
    return cards_dict["UR"] + cards_dict["SSR"] >= n


def is_good_gacha_1(r: requests.Response):
    _, _, _, got_dict = parseGachaResponse(r)
    return has_n_ur_or_ssr(1, got_dict)


def is_good_gacha_10(r: requests.Response, target: int):
    _, _, _, got_dict = parseGachaResponse(r)
    return has_n_ur_or_ssr(target, got_dict)


"""
call gacha1() on s1 only when s2 has a good result
"""


def session_sniffing_1():
    S2_TRIES = 300
    s1 = requests.Session()

    for _ in range(20):
        found_good = False

        for _ in range(S2_TRIES):
            s2 = requests.Session()
            r = gacha1(s2)
            is_good = is_good_gacha_1(r)
            if is_good:
                found_good = True
                break
            time.sleep(0.5)

        if not found_good:
            print("Timout.")
            sys.exit(1)

        r = gacha1(s1)
        info = parseGachaResponse(r)
        print(info)


"""
Optimize by using the 29 gacha method.
"""


def session_sniffing_2():
    GACHA10_ALL_GOOD_TRIES = 1000  # 5/3600 chance of getting 10 UR/SSR
    S2_TRIES = 300  # 106/3600 chance of getting 1 UR/SSR
    s1 = None

    first_10_good = False
    for _ in range(GACHA10_ALL_GOOD_TRIES):
        s1 = requests.Session()
        r = gacha10(s1)
        is_good = is_good_gacha_10(r, 5)

        if is_good:
            first_10_good = True
            break

    if not first_10_good:
        print("First 10 good failed.")
        sys.exit(1)

    print("First 10 gachas has at least 5 UR/SSR.")

    info = ""
    # middle 9 gachas
    for _ in range(9):
        found_good = False

        for _ in range(S2_TRIES):
            s2 = requests.Session()
            r = gacha1(s2)
            is_good = is_good_gacha_1(r)
            if is_good:
                found_good = True
                break
            time.sleep(0.5)

        if not found_good:
            print("Timout.")
            sys.exit(1)

        r = gacha1(s1)
        info = parseGachaResponse(r)
        print(info)

    # we need to have 10 UR/SSR now
    _, inventory, _, _ = info
    if not has_n_ur_or_ssr(10, inventory):
        print("First 19 gachas failed: less than 10 UR/SSR.")
        print(info)
        sys.exit(1)

    good_cards_count = inventory["UR"] + inventory["SSR"]
    print(f"First 19 gachas has at least 10 UR/SSR!")
    print(inventory)

    # last 10 gachas
    is_good = False
    for _ in range(GACHA10_ALL_GOOD_TRIES):
        s2 = requests.Session()
        r = gacha10(s2)
        is_good = is_good_gacha_10(r, 20 - good_cards_count)
        if is_good:
            break

    if not is_good:
        print("Last 10 good failed: not found.")
        sys.exit(1)

    r = gacha10(s1)
    info = parseGachaResponse(r)
    print(info)


def main():
    session_sniffing_2()

if __name__ == "__main__":
    main()
