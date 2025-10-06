import requests
import time
import json

def get_rated_user_handles(max_users=10000):
    """
    Fetches a list of active, rated user handles from Codeforces.
    """
    try:
        print("Fetching a list of rated users...")
        # The user.ratedList endpoint gives us a list of active users.
        url = "https://codeforces.com/api/user.ratedList?activeOnly=true"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        
        data = response.json()
        if data['status'] == 'OK':
            # Extract just the 'handle' from each user object
            handles = [user['handle'] for user in data['result']]
            print(f"Successfully fetched {len(handles)} user handles.")
            return handles[:max_users] # Return the number of users we want
        else:
            print(f"Codeforces API Error: {data.get('comment')}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

def get_user_info_in_batches(handles, batch_size=100):
    """
    Fetches user info for a list of handles in batches to respect API limits.
    """
    all_user_data = []
    # Loop through the handles list in chunks of 'batch_size'
    for i in range(0, len(handles), batch_size):
        # Create a batch of handles
        batch = handles[i:i + batch_size]
        
        # Join handles with a semicolon for the API request
        handles_str = ";".join(batch)
        url = f"https://codeforces.com/api/user.info?handles={handles_str}"
        
        print(f"Fetching batch {i // batch_size + 1}/{(len(handles) + batch_size - 1) // batch_size}...")
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            if data['status'] == 'OK':
                all_user_data.extend(data['result'])
            else:
                print(f"API Error on batch {i}: {data.get('comment')}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred on batch {i}: {e}")
        
        # IMPORTANT: Wait for 2.5 seconds to respect the rate limit
        time.sleep(2.5)
        
    return all_user_data


# --- Main script ---
if __name__ == "__main__":
    # 1. Get the list of user handles
    user_handles = get_rated_user_handles(max_users=10000)
    
    if user_handles:
        # 2. Fetch the detailed info for those handles in batches
        all_users = get_user_info_in_batches(user_handles)
        
        print(f"\nSuccessfully fetched data for {len(all_users)} users.")
        
        # 3. Save the results to a JSON file
        with open("codeforces_user_data.json", "w") as f:
            json.dump(all_users, f, indent=4)
        
        print("Data saved to codeforces_user_data.json")