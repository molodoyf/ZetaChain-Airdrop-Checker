import requests
from time import sleep
import random

def check_airdrop(_wallet: str, proxy: str = None):
    url = f'https://airdrop-router.cl04.zetachain.com/pre-claim-status?address={_wallet}'

    if proxy:
        _proxies = {
            "http": proxy,
            "https": proxy
        }
        response = requests.get(url, proxies=_proxies)
    else:
        response = requests.get(url)

    result = response.json()
    print(f"Wallet: {_wallet}, Result: {result}")
    return result

def save_to_txt(data, wallets, filename="results.txt"):
    with open(filename, "w") as file:
        for i, result in enumerate(data, start=1):
            wallet = wallets[i-1]
            file.write(f"Number: {i}, Wallet: {wallet}, Result: {result}\n")

if __name__ == "__main__":
    results = []
    wallets = []

    with open("wallets.txt", "r") as file:
        wallets = [w.strip() for w in file]

    with open("proxies.txt", "r") as file:
        proxies = [p.strip() for p in file]

    for wallet in wallets:
        try:
            if proxies:
                random_proxy = random.choice(proxies)
                result = check_airdrop(wallet, random_proxy)
            else:
                result = check_airdrop(wallet)

            results.append(result)
        except Exception as e:
            print(f'Failed to check wallet {wallet}, reason: {e}')
        finally:
            sleep(1)

    save_to_txt(results, wallets)
