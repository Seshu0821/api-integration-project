import requests
import json
import os

BASE_URL = "https://jsonplaceholder.typicode.com"

CACHE_FILE = "data.json"

# Save data to local JSON file
def save_cache(data):
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print("Data cached in data.json")

# Load cache data if available
def load_cache():
    if not os.path.exists(CACHE_FILE):
        return None

    with open(CACHE_FILE, "r") as f:
        return json.load(f)

# Fetch posts and users from API
def fetch_data():
    try:
        print("Fetching posts...")
        posts = requests.get(f"{BASE_URL}/posts", timeout=5)
        posts.raise_for_status()

        print("Fetching users...")
        users = requests.get(f"{BASE_URL}/users", timeout=5)
        users.raise_for_status()

        data = {
            "posts": posts.json(),
            "users": users.json(),
        }

        save_cache(data)
        print("API Data fetched successfully!")
        return data

    except requests.exceptions.Timeout:
        print("Error: Request timed out.")
    except requests.exceptions.ConnectionError:
        print("Network error. Check your internet.")
    except requests.exceptions.HTTPError:
        print("Invalid HTTP response.")
    except Exception as e:
        print(f"Unexpected error: {e}")



# List all posts (with optional filtering)
def list_posts(user_id=None):
    data = load_cache()
    if not data:
        print("No cached data found. Fetching now…")
        data = fetch_data()

    posts = data["posts"]

    if user_id:
        posts = [p for p in posts if p["userId"] == user_id]

    if posts:
        for post in posts[:10]:  # limit output
            print(f"[ID: {post['id']}] {post['title']}")
    else:
        print("No Posts Found")

# Get single post by ID
def get_post(post_id):
    data = load_cache()
    if not data:
        print("No cached data found. Fetching now…")
        data = fetch_data()

    posts = data["posts"]

    result = next((p for p in posts if p["id"] == post_id), None)

    if result:
        print(json.dumps(result, indent=4))
    else:
        print("Post not found")


# Get user details by ID
def get_user(user_id):
    data = load_cache()
    if not data:
        print("No cached data found. Fetching now…")
        data = fetch_data()

    users = data["users"]

    result = next((u for u in users if u["id"] == user_id), None)

    if result:
        print(json.dumps(result, indent=4))
    else:
        print("User not found")


# Main Menu
def menu():
    while True:
        print("\n====== API DATA FETCHER ======")
        print("1. Fetch and cache data")
        print("2. List posts")
        print("3. List posts filtered by userId")
        print("4. Get post by ID")
        print("5. Get user by ID")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            print()
            fetch_data()

        elif choice == "2":
            print()
            list_posts()
            

        elif choice == "3":
            user_id = int(input("Enter userId: "))
            print()
            list_posts(user_id=user_id)

        elif choice == "4":
            post_id = int(input("Enter post ID: "))
            print()
            get_post(post_id)

        elif choice == "5":
            user_id = int(input("Enter user ID: "))
            print()
            get_user(user_id)

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    menu()
