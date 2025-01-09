import requests
import json
import argparse
import os
from dotenv import load_dotenv

# API URL
load_dotenv('/home/josh/Documents/Projects/blog_rest_api/db_config.env') # Change this to your .env path
BASE_URL = os.getenv('BASE_URL')
if not BASE_URL:
    print("Base url not found!")

# Fetches blog data from REST API
def fetch_blogs():
    response = requests.get(f"{BASE_URL}/blogs")
    if response.status_code == 200:
        blogs = response.json()
        return blogs
    else:
        print(f"Failed to fetch blogs: {response.status_code}")
        return []

# Fetches user data from REST API
def fetch_users():
    response = requests.get(f"{BASE_URL}/users")
    if response.status_code == 200:
        users = response.json()
        return users

# Deletes blog from ID
def delete_blog(blog_id):
    response = requests.delete(f"{BASE_URL}/users/{blog_id}")
    if response.status_code == 200:
        print(f"Blog {blog_id} deleted successfully.")
    else:
        print(f"Failed to delete blog {blog_id}: {response.json()}")

# Deletes user from ID        
def delete_user(user_id):
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    if response.status_code == 200:
        print(f"Blog {user_id} deleted successfully.")
    else:
        print(f"Failed to delete blog {user_id}: {response.json()}")

# Adds a user with <name> <email> <password_hash>
def add_user(name, email, password_hash):
    response = requests.post(f"{BASE_URL}/users", json={"username": name, "email": email, "password_hash": password_hash})
    if response.status_code == 201:
        print("User created successfully.")
    else:
        print("Response content:", response.text)
        try:
            print(f"Failed to create user: {response.json()}")
        except ValueError:
            print("Response is not in JSON format.")

def add_blog(title, content):
    response = requests.post(f"{BASE_URL}/posts", json={"title": title, "content": content})
    if response.status_code == 201:
        print("Blog created successfully.")
    else:
        print("Response content:", response.text)
        try:
            print(f"Failed to create Blog: {response.json()}")
        except ValueError:
            print("Response is not in JSON format.")

def update_user(user_id, name, email, password_hash):
    response = requests.put(f"{BASE_URL}/users/{user_id}", 
    json={
        "username": name,
        "email": email,
        "password_hash": password_hash
        }
    )
    
    if response.status_code in (200, 204):
        print("User updated successfully.")
    else:
        print("Response content:", response.text)
        try:
            print(f"Failed to update User: {response.json()}")
        except ValueError:
            print("Response is not in JSON format.")

def update_blog(blog_id, title, content):
    response = requests.put(f"{BASE_URL}/posts/{blog_id}", json={
        "title": title,
        "content": content
    })
    
    if response.status_code in (200, 204):
        print("Blog updated successfully.")
    else:
        print("Response content:", response.text)
        try:
            print(f"Failed to update Blog: {response.json()}")
        except ValueError:
            print("Response is not in JSON format.")

# Build application
if __name__=="__main__":
    
    # CLI arguments
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--delete", action='store_true', help="Delete an item.")
    
    parser.add_argument("--user", type=int, help="ID of the user to delete.")
    
    parser.add_argument("--blog", type=int, help="ID of the blog to delete.")
    
    parser.add_argument("--create_user", type=str, nargs=3, help="Create a new user with <name> <email> <password>")
    
    parser.add_argument("--create_blog", type=str, nargs=2, help="Create a blog with <title> <content>")
    
    parser.add_argument("--update", action='store_true', help="Update an item")
    
    parser.add_argument("-u", type=str, nargs=3, help="User parameters <name> <email> <password_hash>")
    
    parser.add_argument("-b", type=str, nargs=2, help="Blog prameters <title> <content>")
    
    args = parser.parse_args()
    
    # Delete a user
    if args.delete and args.user:
        delete_user(args.user)
    # Delete a blog
    if args.delete and args.blog:
        delete_blog(args.blog)
    # Create a user
    if args.create_user:
        add_user(args.create_user[0], args.create_user[1], args.create_user[2])
    # Create a blog
    if args.create_blog:
        add_blog(args.create_blog[0], args.create_blog[1])
    # Update a user
    if args.update and args.user and args.u:
        update_user(args.user, args.u[0], args.u[1], args.u[2])
    # Update a blog
    if args.update and args.blog and args.b:
        update_blog(args.blog, args.b[0], args.b[1])