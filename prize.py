import requests
import json
import time
import os

# ============================================================
# COLORS (No Red / Pink / Magenta)
# ============================================================

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
WHITE = "\033[97m"
RESET = "\033[0m"

# ============================================================
# SIMPLE LOGO
# ============================================================

print(f"""
{CYAN}==============================
     PRIZENOVA BOT TOOL
      Code2Crypto
      Developed By Anaik_Dev
=============================={RESET}
""")

# ============================================================
# CONFIGURATION
# ============================================================

BASE_URL = 'https://prizenova.top/app/api/'
REFERRAL_LINK = "https://t.me/PrizeNovaBot?startapp=3bYtcsOFTl"
QUERY_FILE = "Query.txt"

HEADERS = {
    'authority': 'prizenova.top',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'cookie': 'SITE_TOTAL_ID=393b15fa0e6e6c6ed133171cbfead153',
    'origin': 'https://prizenova.top',
    'referer': 'https://prizenova.top/app/index.html',
    'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
}

# ============================================================
# GET QUERY IDS
# ============================================================

def get_query_ids():

    print(f"{WHITE}Choose Mode:{RESET}")
    print(f"{CYAN}[1] Single Query ID")
    print(f"[2] Multiple IDs (save to Query.txt)")
    print(f"[3] Run using saved Query.txt{RESET}")

    choice = input(f"\n{YELLOW}Enter option (1/2/3): {RESET}").strip()

    if choice == "1":
        qid = input(f"{YELLOW}Enter your QUERY ID: {RESET}").strip()
        if not qid:
            print(f"{YELLOW}No Query ID entered. Exiting...{RESET}")
            exit()
        return [qid]

    elif choice == "2":
        print(f"{CYAN}Enter multiple Query IDs (one per line). Type 'done' when finished:{RESET}")

        qids = []
        while True:
            q = input("> ").strip()
            if q.lower() == "done":
                break
            if q:
                qids.append(q)

        if not qids:
            print(f"{YELLOW}No Query IDs entered.{RESET}")
            exit()

        with open(QUERY_FILE, "w") as f:
            for q in qids:
                f.write(q + "\n")

        print(f"{GREEN}Saved {len(qids)} IDs to {QUERY_FILE}{RESET}")
        return qids

    elif choice == "3":
        if not os.path.exists(QUERY_FILE):
            print(f"{YELLOW}Query.txt not found!{RESET}")
            exit()

        with open(QUERY_FILE, "r") as f:
            qids = [line.strip() for line in f if line.strip()]

        print(f"{GREEN}Loaded {len(qids)} IDs from {QUERY_FILE}{RESET}")
        return qids

    else:
        print(f"{YELLOW}Invalid choice! Exiting...{RESET}")
        exit()

# ============================================================
# FETCH TASKS
# ============================================================

def get_tasks(query_id):
    print(f"\n{CYAN}Fetching tasks...{RESET}")
    url = BASE_URL + 'get_tasks.php'
    payload = {"init_data": query_id}

    try:
        response = requests.post(url, headers=HEADERS, data=json.dumps(payload))
        response.raise_for_status()

        data = response.json()

        if not data.get('ok'):
            print(f"{YELLOW}Invalid Query ID or session expired.{RESET}")
            return []

        tasks_container = data.get('data') or {}
        all_tasks = []

        for v in tasks_container.values():
            if isinstance(v, list):
                all_tasks.extend(v)

        unique = {task.get('id'): task for task in all_tasks if task.get('id')}
        sorted_tasks = sorted(unique.values(), key=lambda x: int(x.get('id', 0)))

        print(f"{GREEN}Tasks found: {len(sorted_tasks)}{RESET}")
        return sorted_tasks

    except Exception as e:
        print(f"{YELLOW}Error fetching tasks: {e}{RESET}")
        return []

# ============================================================
# COMPLETE TASK
# ============================================================

def complete_task(query_id, task_id):

    url = BASE_URL + 'complete-task.php'
    payload = {"init_data": query_id, "task_id": str(task_id)}

    try:
        response = requests.post(url, headers=HEADERS, data=json.dumps(payload))
        response.raise_for_status()

        data = response.json()

        if data.get('success'):
            print(f"{GREEN}Task {task_id} done!{RESET}")
        else:
            print(f"{YELLOW}Task {task_id} failed: {data.get('message', data)}{RESET}")

    except Exception as e:
        print(f"{YELLOW}Error completing task {task_id}: {e}{RESET}")

# ============================================================
# DASHBOARD (with your referral)
# ============================================================

def get_dashboard(query_id):

    print(f"\n{CYAN}Fetching dashboard info...{RESET}")

    url = BASE_URL + 'dashboard.php'
    payload = {
        "init_data": query_id,
        "invited_by": REFERRAL_LINK
    }

    try:
        response = requests.post(url, headers=HEADERS, data=json.dumps(payload))
        response.raise_for_status()

        data = response.json()
        user = data.get('data') or {}
        coins = user.get('draw_total_coin', 'N/A')

        print(f"""
{WHITE}----------------------------
   ACCOUNT SUMMARY
----------------------------
Coins: {coins}
----------------------------{RESET}
""")

    except Exception as e:
        print(f"{YELLOW}Dashboard error: {e}{RESET}")

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print(f"{CYAN}======================================{RESET}")
    print(f"{WHITE}Starting Prizenova Multi Bot...{RESET}")
    print(f"{CYAN}======================================{RESET}")

    query_ids = get_query_ids()

    for i, qid in enumerate(query_ids, start=1):

        print(f"\n{CYAN}--------------------------{RESET}")
        print(f"{WHITE}PROCESSING ID {i}/{len(query_ids)}{RESET}")
        print(f"{CYAN}--------------------------{RESET}")

        tasks = get_tasks(qid)

        if tasks:
            print(f"\n{GREEN}Completing tasks...{RESET}\n")
            for task in tasks:
                tid = task.get('id')
                name = task.get('name', f"Task {tid}")
                if tid:
                    print(f"{WHITE}▶ {name} (ID: {tid}){RESET}")
                    complete_task(qid, tid)
                    time.sleep(2)
            print(f"{GREEN}All tasks done for this account!{RESET}")
        else:
            print(f"{YELLOW}No tasks to complete for this ID.{RESET}")

        get_dashboard(qid)

    print(f"\n{CYAN}======================================{RESET}")
    print(f"{GREEN}ALL ACCOUNTS PROCESSED SUCCESSFULLY!{RESET}")
    print(f"{CYAN}======================================{RESET}\n")