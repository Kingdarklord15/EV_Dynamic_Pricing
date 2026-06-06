import requests
import pandas as pd
import time

TOKEN = "6nIRhdftYQ5UPTKSSaONj9sAU98RyxkIyXFoa-HIN7I"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

all_records = []

for page in range(1, 401):

    try:
        url = f"https://ev.caltech.edu/api/v1/sessions/caltech?page={page}"

        response = requests.get(url, headers=headers, timeout=60)

        if response.status_code != 200:
            print(f"Page {page} returned {response.status_code}")
            continue

        data = response.json()

        all_records.extend(data["_items"])

        if page % 25 == 0:

            df = pd.json_normalize(all_records)

            df.to_csv("acn_partial.csv", index=False)

            print(
                f"Page {page} | Records: {len(all_records)} | Backup Saved"
            )

        time.sleep(0.2)

    except Exception as e:
        print(f"Error on page {page}: {e}")

df = pd.json_normalize(all_records)

df.to_csv("acn_full.csv", index=False)

print(df.shape)