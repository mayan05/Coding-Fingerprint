import requests
import time
import csv
import os

# --- Configuration ---
TOTAL_HANDLES_TO_PROCESS = 30000
OUTPUT_CSV_FILE = 'codeforces_filtered_users.csv'
BATCH_SIZE = 500 # Number of users to fetch in a single API call

def get_all_rated_handles(max_handles):
    """
    Fetches a list of all active, rated user handles from the Codeforces API.
    This provides the pool of users we will get details for.
    """
    print(f"Fetching up to {max_handles} rated user handles from Codeforces...")
    try:
        url = "https://codeforces.com/api/user.ratedList?activeOnly=true"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        data = response.json()
        if data['status'] == 'OK':
            handles = [user['handle'] for user in data['result']]
            print(f"Successfully fetched {len(handles)} total rated handles.")
            return handles[:max_handles]
        else:
            print(f"Codeforces API Error: {data.get('comment')}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"A network error occurred while fetching user list: {e}")
        return []

def fetch_and_save_users_to_csv(handles):
    """
    Fetches user info in batches and saves valid users directly to a CSV file.
    A user is valid if they have both a 'rank' and a 'country'.
    """
    # Define the columns for the CSV file
    csv_columns = ['Handle', 'Rank', 'Country']
    
    # Counter for valid users found
    valid_users_count = 0
    
    print(f"\nProcessing {len(handles)} handles. This will take approximately {((len(handles)/BATCH_SIZE)*2)/60:.1f} minutes.")

    # Open the CSV file in write mode to add the header
    # 'newline=""' is important to prevent extra blank rows in the CSV
    with open(OUTPUT_CSV_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        
        # Loop through all handles in batches
        num_batches = (len(handles) + BATCH_SIZE - 1) // BATCH_SIZE
        for i in range(0, len(handles), BATCH_SIZE):
            batch_handles = handles[i:i + BATCH_SIZE]
            handles_str = ";".join(batch_handles)
            url = f"https://codeforces.com/api/user.info?handles={handles_str}"
            
            print(f"Processing Batch {i // BATCH_SIZE + 1}/{num_batches}...")
            
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                
                if data['status'] == 'OK':
                    # Process each user in the returned batch
                    for user in data['result']:
                        # THE CORE LOGIC: Check if both rank and country exist
                        if 'rank' in user and 'country' in user:
                            writer.writerow({
                                'Handle': user['handle'],
                                'Rank': user['rank'],
                                'Country': user['country']
                            })
                            valid_users_count += 1
                else:
                    print(f"  -> API Error on batch: {data.get('comment')}")

            except requests.exceptions.RequestException as e:
                print(f"  -> Network error on batch: {e}")

            # IMPORTANT: Wait 2 seconds due to the API rate limit
            time.sleep(2)
            
    print("\n--- Process Complete ---")
    print(f"Finished processing all batches.")
    print(f"Found and saved {valid_users_count} users with both rank and country.")
    print(f"Data is saved in '{OUTPUT_CSV_FILE}'")


# --- Main script execution ---
if __name__ == "__main__":
    # 1. Get the pool of user handles to process
    handles_to_process = get_all_rated_handles(max_handles=TOTAL_HANDLES_TO_PROCESS)
    
    if handles_to_process:
        # 2. Fetch data in batches and save valid users directly to CSV
        fetch_and_save_users_to_csv(handles_to_process)
    else:
        print("Could not fetch user handles. Halting execution.")