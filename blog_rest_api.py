from flask import Flask, request, jsonify
import mysql.connector
import ssl
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/home/josh/Documents/Projects/blog_rest_api/db_config.env') # Change this to your .env path

# Create Flask application
app = Flask(__name__)

DB_HOST = os.getenv('DB_HOST')         # Host AWS in my case
DB_USER = os.getenv('DB_USER')         # Username
DB_PASSWORD = os.getenv('DB_PASSWORD') # Password
DB_NAME = os.getenv('DB_NAME')         # Database name
DB_SSL_PATH = os.getenv('DB_SSL_PATH') # SSL file - required
BASE_URL = os.getenv('BASE_URL')       # Base URL for the REST API

@app.route('/blogs', methods=['GET'])
def get_blogs():
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            ssl_ca=DB_SSL_PATH
        )
        
        # Create cursor
        cursor = connection.cursor(dictionary=True)  # Get column names
        
        # Execute cursor
        cursor.execute("SELECT * FROM posts")
        
        # Fetch all rows from the table
        blogs = cursor.fetchall()
        
        # Close the connection
        cursor.close()
        connection.close()
        
        # Return the data as JSON
        return jsonify(blogs)
    
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

@app.route('/users', methods=['GET'])
def get_users():
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            ssl_ca=DB_SSL_PATH
        )
        cursor = connection.cursor(dictionary=True)  # Use dictionary=True to get column names
        cursor.execute("SELECT * FROM users")
        
        users = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify(users)
    
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

@app.route('/blogs/<int:blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            ssl_ca=DB_SSL_PATH
        )
        
        cursor = connection.cursor()
        
        query = "DELETE FROM blogs WHERE id = %s"
        cursor.execute(query, (blog_id,))
        
        connection.commit()
        
        # Check if data is available
        if cursor.rowcount == 0:
            return {"error": "Blog not found"}, 404 # No data error
        return {"message": "Blog deleted successfully"}
    
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            ssl_ca=DB_SSL_PATH
        )
        cursor = connection.cursor()
        
        query = "DELETE FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        
        connection.commit()
        
        if cursor.rowcount == 0:
            return {"error": "User not found"}, 404
        return {"message": "User deleted succesfully"}
    
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('username')
    email = data.get('email')
    password_hash = data.get('password_hash')
    
    if not name or not email or not password_hash:
        return jsonify({"error": "Name, email and password are required."}), 400
    
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            ssl_ca=DB_SSL_PATH
        )
        cursor = connection.cursor()
        query = 'INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)'
        cursor.execute(query, (name, email, password_hash))
        connection.commit()
        return jsonify({"message": "User created successfully"}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

@app.route('/posts', methods=['POST'])
def create_blog():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    
    if not title or not content:
        return jsonify({"error": "Titl and content are required."}), 400
    
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            ssl_ca=DB_SSL_PATH
        )
        cursor = connection.cursor()
        query = 'INSERT INTO posts (title, content) VALUES (%s, %s)'
        cursor.execute(query, (title, content))
        connection.commit()
        return jsonify({"message": "Blog created successfully"}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name = data.get('username')
    email = data.get('email')
    password_hash = data.get('password_hash')
    
    if not name or not email or not password_hash:
        return jsonify({"error": "Name, email and password are required."}), 400
    
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            ssl_ca=DB_SSL_PATH
        )
        cursor = connection.cursor()
        
        # Update query
        query = """
        UPDATE users
        SET username = %s, email = %s, password_hash = %s
        WHERE id = %s
        """
        
        # Execute query
        cursor.execute(query, (name, email, password_hash, user_id))
        connection.commit()
        
        # Check if any row was affected (user_id exists)
        if cursor.rowcount == 0:
            return jsonify({"error": "User not found."}), 404

        return jsonify({"message": "User updated successfully"}), 200
    
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    
    finally:
        cursor.close()
        connection.close()

@app.route('/posts/<int:blog_id>', methods=['PUT'])
def update_blog(blog_id):
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    
    if not title or not content:
        return jsonify({"error": "Title and content are required."}), 400
    
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            ssl_ca=DB_SSL_PATH
        )
        cursor = connection.cursor()
        
        # Update query
        query = """
        UPDATE posts
        SET title = %s, content = %s
        WHERE id = %s
        """
        
        # Execute query
        cursor.execute(query, (title, content, blog_id))
        connection.commit()
        
        # Check if any row was affected (user_id exists)
        if cursor.rowcount == 0:
            return jsonify({"error": "Blog not found."}), 404

        return jsonify({"message": "Blog updated successfully"}), 200
    
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    
    finally:
        cursor.close()
        connection.close()

# Build application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)