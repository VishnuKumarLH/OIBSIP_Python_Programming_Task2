# 🧮 BMI Calculator with GUI

A **Graphical BMI Calculator** built using **Python (Tkinter, SQLite, Matplotlib)** that allows users to calculate their BMI, store records, view history, and analyze BMI trends with graphs.

---

## ✨ Features
- ✅ User-friendly **GUI with Tkinter**
- ✅ **BMI calculation** with health category classification
- ✅ **Input validation** (Weight: 30–300 kg, Height: 100–250 cm)
- ✅ **Data storage** with SQLite (saves username, weight, height, BMI, and timestamp)
- ✅ **View historical data** in a table with scrollbar
- ✅ **BMI trend analysis** with Matplotlib graphs
- ✅ **Statistics**: Minimum, Maximum, and Average BMI
- ✅ **Delete history** for a specific user

---

## 🖼️ Demo Video
🎥 [Watch Demo Video](https://youtu.be/your-demo-video-link)  
*(Replace the above link with your actual uploaded video on YouTube/Drive/LinkedIn)*

---

## 📸 Screenshots
### BMI Calculation  
![BMI Calculation Screenshot](./dashboard)  

### BMI Trend Graph  
![BMI Graph Screenshot](./graph)  

---

## ⚙️ Installation & Usage

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/bmi_calculator.git
cd bmi_calculator
```

### 2️⃣ Install Requirements
```bash
pip install matplotlib
```
*(Tkinter and SQLite come pre-installed with Python.)*

### 3️⃣ Run the Application
```bash
python bmi_calculator.py
```

---

## 📂 Project Structure
```
bmi_calculator/
│── bmi_calculator.py   # Main application code
│── bmi_records.db      # SQLite database (auto-created)
│── README.md           # Project documentation
```

---

## 🧮 BMI Formula
\[
BMI = \frac{Weight (kg)}{Height (m)^2}
\]

**Categories:**
- Underweight: < 18.5  
- Normal: 18.5 – 24.9  
- Overweight: 25 – 29.9  
- Obese: 30+  

---

## 📊 Example Statistics
- **Min BMI**: 18.20  
- **Max BMI**: 28.50  
- **Average BMI**: 23.40  

---

## 🛠️ Tech Stack
- **Python 3**
- **Tkinter** – GUI  
- **SQLite** – Data storage  
- **Matplotlib** – Graphs and statistics  

---

## 🤝 Contributing
Pull requests are welcome. For major changes, open an issue first to discuss what you’d like to change.

---

## 📜 License
This project is licensed under the MIT License.

---
