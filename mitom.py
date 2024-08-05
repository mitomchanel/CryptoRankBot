import requests
import time
import os
from colorama import Fore, Style, init
from datetime import timedelta

init(autoreset=True)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_welcome_message():
    print("\033[1;91m" + r""" 
 __  __ _ _                     ____ _                      _ 
|  \/  (_) |_ ___  _ __ ___    / ___| |__   __ _ _ __   ___| |
| |\/| | | __/ _ \| '_ ` _ \  | |   | '_ \ / _` | '_ \ / _ \ |
| |  | | | || (_) | | | | | | | |___| | | | (_| | | | |  __/ |
|_|  |_|_|\__\___/|_| |_| |_|  \____|_| |_|\__,_|_| |_|\___|_|

Crypro Rank Bot

""" + "\033[0m")
# Load tokens from data.txt
with open('data.txt', 'r') as file:
    tokens = [line.strip() for line in file.readlines()]

# Headers template for the requests
headers_template = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "pragma": "no-cache",
    "sec-ch-ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "referrer": "https://tma.cryptorank.io/",
    "referrerPolicy": "strict-origin-when-cross-origin",
    "credentials": "include"
}

# URLs for the requests
login_url = "https://api.cryptorank.io/v0/tma/account"
end_farming_url = "https://api.cryptorank.io/v0/tma/account/end-farming"
start_farming_url = "https://api.cryptorank.io/v0/tma/account/start-farming"
claim_buddies_url = "https://api.cryptorank.io/v0/tma/account/claim/buddies"
task_claim_url = "https://api.cryptorank.io/v0/tma/account/claim/task/"

tasks = [
    "2a6855fa-1308-4548-b7c3-4852e6cc6c46",
    "324dc84b-9bea-433c-8035-8d1c161727d8",
    "5c47ecc7-547a-4f71-ba3f-b19651a5b773",
    "9b089eb5-a104-4358-9847-980965e1f19d",
    "cfb01d3d-cb3d-4427-aa68-3eeb26990672",
    "d40e284f-c389-4d49-b8d7-98d3c8a745ab",
    "db9876de-4b43-460e-b725-18e4ca6a0285",
    "dedafce3-4658-4eb4-bad5-f29b6cc500c9",
    "df61ebb0-ae37-4ba2-b6bb-f41cef4a27c0",
    "e7dae272-7d17-4543-9a30-92f071439210"
]

# Prompt for auto task claim
clear_terminal()
print_welcome_message()
auto_claim_task = input("Do you want auto claim ask? (y/n): ").strip().lower()
clear_terminal()

while True:
    clear_terminal()
    print_welcome_message()
    
    for index, token in enumerate(tokens, start=1):
        headers = headers_template.copy()
        headers["authorization"] = token

        # Log in to the account
        response = requests.get(login_url, headers=headers)
        if response.status_code == 200:
            account_data = response.json()
            balance = account_data.get('balance', 'Unknown')

            print(f"{Fore.CYAN + Style.BRIGHT}------Account {index}------") 
            print(f"{Fore.YELLOW + Style.BRIGHT}Balance: {balance}")

            # End farming to claim rewards
            response = requests.post(end_farming_url, headers=headers)
            if response.status_code == 201:
                print(f"{Fore.GREEN + Style.BRIGHT}Farming Claim Successful")
            elif response.status_code == 409:
                print(f"{Fore.RED + Style.BRIGHT}Farming Already Claimed")
            else:
                print(f"{Fore.RED + Style.BRIGHT}Failed to claim farming: {response.status_code}")

            # Start farming again
            response = requests.post(start_farming_url, headers=headers)
            if response.status_code == 201:
                print(f"{Fore.GREEN + Style.BRIGHT}Farming Start Successful")
            elif response.status_code == 409:
                print(f"{Fore.RED + Style.BRIGHT}Farming Already Started")
            else:
                print(f"{Fore.RED + Style.BRIGHT}Failed to start farming: {response.status_code}")

            # Claim buddies
            response = requests.post(claim_buddies_url, headers=headers)
            if response.status_code == 201:
                print(f"{Fore.GREEN + Style.BRIGHT}Buddies Claim Successful")
            elif response.status_code == 409:
                print(f"{Fore.RED + Style.BRIGHT}Buddies Already Claimed")
            else:
                print(f"{Fore.RED + Style.BRIGHT}Failed to claim buddies: {response.status_code}")

            # Auto task claim if requested
            if auto_claim_task == 'y':
                for task_id in tasks:
                    claim_task_response = requests.post(task_claim_url + task_id, headers=headers)
                    if claim_task_response.status_code == 201:
                        task_name = claim_task_response.json().get('name', 'Unknown Task')
                        print(f"{Fore.GREEN + Style.BRIGHT}Task Claimed Successful")
                    elif claim_task_response.status_code == 409:
                        task_name = claim_task_response.json().get('name', 'Unknown Task')
                        print(f"{Fore.RED + Style.BRIGHT}Task Already Claimed")
                    else:
                        print(f"{Fore.RED + Style.BRIGHT}Failed to claim task")

            print("\n")

        else:
            print(f"{Fore.RED + Style.BRIGHT}Failed to log in with token: {token}, status code: {response.status_code}")

        # Countdown before processing the next account
        if index < len(tokens):  # Only wait if there are more accounts to process
            countdown_msg = f"Wait "
            for remaining_seconds in range(5, 0, -1):
                print(f"\r{Fore.MAGENTA + Style.BRIGHT}{countdown_msg}{remaining_seconds} seconds", end='')
                time.sleep(1)
            print("\n")

    # Countdown before starting the next cycle
    countdown_msg = f"Wait "
    for remaining_seconds in range(10800, 0, -1):
        remaining_time = str(timedelta(seconds=remaining_seconds))
        print(f"\r{Fore.MAGENTA + Style.BRIGHT}{countdown_msg}{remaining_time}", end='')
        time.sleep(1)
    print("\n")
