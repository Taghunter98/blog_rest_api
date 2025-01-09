# Blog REST API

A Flask-based RESTful API that interacts with a MySQL database to manage users and blog entries. This project is hosted on AWS RDS for the database and allows for CRUD operations through endpoints.

## Features

- **User Management**: Add, retrieve, update, and delete user data.
- **Blog Management**: Add, retrieve, update, and delete blog entries.
- **Secure Database Connection**: Uses environment variables and SSL for database connections.
- **Scalable Design**: Built with RESTful principles to support future expansion.

## Getting Started

### Prerequisites

- Python 3.10 or above
- Virtual Environment (`venv`)
- Flask (`pip install flask`)
- Requests (`pip install requests`)
- dotenv (`pip install python-dotenv`)
- MySQL server

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Taghunter98/blog-rest-api.git
   cd blog-rest-api
   ```

2. **Set Up Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # For Linux/MacOS
   venv\Scripts\activate      # For Windows
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   - Create a `.env` file in the project directory with the following format:
     ```
     DB_HOST='your-rds-endpoint.amazonaws.com'
     DB_USER='your-db-username'
     DB_PASSWORD='your-db-password'
     DB_NAME='your-db-name'
     DB_SSL_PATH='/path-to-your-ssl-certificate.pem'
     BASE_URL='http://127.0.0.1:5000'
     ```

5. **Run the Flask Server**
   ```bash
   flask run
   ```

## Usage

### API Endpoints

#### Users

- **Create a User**: `POST /users`
- **Retrieve Users**: `GET /users`
- **Update a User**: `PUT /users/<id>`
- **Delete a User**: `DELETE /users/<id>`

#### Blogs

- **Create a Blog**: `POST /blogs`
- **Retrieve Blogs**: `GET /blogs`
- **Update a Blog**: `PUT /blogs/<id>`
- **Delete a Blog**: `DELETE /blogs/<id>`

---

### CLI Script for Interacting with API

A Python script (`fetch_blog_data.py`) is included for interacting with the API via the command line.

#### Examples:

1. **Create a User**
   ```bash
   python fetch_blog_data.py --create_user "Steve" "steve@example.com" "password123"
   ```
2. **Create a Blog**
   ```bash
   python fetch_blog_data.py --create_blog "Learning Python The Hard Way" "I decided to learn Python the hard way... The end"
   ```
3. **Delete a User or Blog**
   ```bash
   python fetch_blog_data.py --delete --blog 1 # User ID
   python fetch_blog_data.py --delete --user 1 # Blog ID
   ```
4. **Update a User or Blog**

   ```bash
   python fetch_blog_data.py --update --blog 1 -u "Josh" "coolemail@gmail.com" "super_secure_password123"

   python fetch_blog_data.py --update --user -b "My First Blog" "Today I wrote 'Hello World and printed it on the console...'"
   ```

   Use the `--update` and `-u` or `-b` flag and pass the blog and `user_id` followed by the new name, email and password.

## Deployment

### AWS RDS Setup

Ensure your AWS RDS instance allows connections from your IP address and uses SSL for secure communication.

---

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request with detailed explanations for your changes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/) for the web framework.
- [MySQL](https://www.mysql.com/) for the database.
- [AWS RDS](https://aws.amazon.com/rds/) for hosting the database.

---
