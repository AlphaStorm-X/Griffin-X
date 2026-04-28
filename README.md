# 🩺 AuraCare

A full-stack healthcare management web application that helps users manage medical records, track medicines, and gain insights from their health reports.

---

## 🚀 Features

* 🔐 User Authentication (JWT-based)
* 💊 Medicine Tracking & Reminders
* 📄 Upload & Analyze Medical Reports *(planned/extendable)*
* 📊 Dashboard for health overview
* 🗂️ Secure storage of patient records

---

## 🛠️ Tech Stack

### Frontend

* React.js
* Tailwind CSS
* Vite

### Backend

* FastAPI (Python)
* MongoDB
* JWT Authentication

---

## 📁 Project Structure

```
Auracare/
│
├── src/                 # Frontend (React)
├── public/              # Static files
├── app/                 # Backend (FastAPI)
├── requirements.txt     # Python dependencies
├── package.json         # Frontend dependencies
├── .env.example         # Environment variables template
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```
git clone https://github.com/AlphaStorm-X/Auracare.git
cd Auracare
```

---

### 2️⃣ Setup Frontend

```
npm install
npm run dev
```

---

### 3️⃣ Setup Backend

```
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 🔐 Environment Variables

Create a `.env` file in the root directory and add:

```
MONGO_URI=your_mongo_uri
JWT_SECRET=your_secret_key
OPENAI_API_KEY=your_api_key (optional)
```

⚠️ Do NOT commit `.env` file to GitHub.

---

## 👥 Collaboration Workflow

* Always pull latest changes before working:

  ```
  git pull origin main
  ```

* Create a new branch for features:

  ```
  git checkout -b feature-name
  ```

* Push your branch and create a Pull Request

---

## 🌍 Future Enhancements

* AI-based report analysis
* Notification system for medicines
* Cloud deployment
* Role-based access (Doctor/Patient)

---

## 📌 Contribution

Contributions are welcome! Feel free to fork the repo and submit pull requests.

---

## 📄 License

This project is licensed under the MIT License.

---

## ✨ Author

Griffin-X

---

## ⭐ Support

If you like this project, consider giving it a star ⭐ on GitHub!
