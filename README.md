# 🎨 AI Image Generator Web Application

A Flask-based web application that allows users to create AI-generated images in different artistic styles such as **Anime**, **Cartoon**, and **Comic**. The application includes user authentication, prompt history storage, and AI-powered image generation using the ClipDrop Text-to-Image API.

---

## 🚀 Features

* User Registration and Login System
* Secure Password Hashing using Bcrypt
* Session Management with Flask-Login
* AI Image Generation from Text Prompts
* Multiple Art Styles:

  * Anime
  * Cartoon
  * Comic
* MySQL Database Integration
* Prompt Storage and Tracking
* Generated Images Saved Locally
* Responsive Dashboard Interface

---

## 🛠️ Tech Stack

### Backend

* Flask
* Flask-Login
* Flask-MySQLdb
* Flask-Bcrypt

### Database

* MySQL

### Frontend

* HTML
* CSS

### API

* ClipDrop Text-to-Image API

---

## 📂 Project Structure

```text
├── static/
│   ├── ce6e626ddc04423c9b0586de1297c805.png
│   ├── dash.css
│   ├── main.css
│   └── style.css
│
├── templates/
│   ├── login.html
│   ├── Signup.html
│   └── Main.html
│
├── database.db
├── main.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-image-generator.git
cd ai-image-generator
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/Mac

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL Database

Create a MySQL database:

```sql
CREATE DATABASE login_details;
```

Create the required tables:

```sql
CREATE TABLE details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255)
);

CREATE TABLE prompts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT,
    type VARCHAR(50),
    email VARCHAR(255)
);
```

### 5. Update Database Credentials

Modify the following section in `main.py`:

```python
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "your_username"
app.config['MYSQL_PASSWORD'] = "your_password"
app.config['MYSQL_DB'] = "login_details"
```

### 6. Add ClipDrop API Key

Replace the API key in `main.py`:

```python
headers={
    "x-api-key": "YOUR_CLIPDROP_API_KEY"
}
```

---

## ▶️ Running the Application

```bash
python main.py
```

The application will be available at:

```text
http://127.0.0.1:5000
```

---

## 🎯 Usage

1. Register a new account.
2. Login with your credentials.
3. Enter a text prompt.
4. Select an image style:

   * Anime
   * Cartoon
   * Comic
5. Generate the image.
6. View and download the generated image.

---

## 🔒 Security Notes

* Passwords are hashed using Bcrypt before storage.
* Login sessions are managed securely with Flask-Login.
* Never commit API keys or database credentials to public repositories.
* Use environment variables for sensitive information in production.

Example:

```python
import os

API_KEY = os.getenv("CLIPDROP_API_KEY")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
```

---

## 📋 Requirements

Example dependencies:

```txt
Flask
Flask-Login
Flask-MySQLdb
Flask-Bcrypt
requests
mysqlclient
```

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔮 Future Enhancements

* Image Download Button
* User Prompt History Page
* Image Gallery
* Dark Mode UI
* Email Verification
* Password Reset Functionality
* Cloud Image Storage (AWS S3 / Cloudinary)
* Multiple AI Model Support

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push to your branch.
5. Open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

Developed using Flask, MySQL, and ClipDrop AI API.
