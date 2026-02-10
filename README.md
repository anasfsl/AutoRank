# AutoRank: Intelligent Car Recommendation Engine 🚗

A decision-support tool that ranks vehicles based on conflicting user criteria (Price vs. Performance) using the **TOPSIS Algorithm**.

## 🚀 Features
- **Multi-Criteria Decision Making:** Uses the TOPSIS algorithm (Technique for Order of Preference by Similarity to Ideal Solution) to mathematically rank options.
- **Vectorized Processing:** Leverages **Pandas** and **NumPy** for high-performance data normalization and Euclidean distance calculations.
- **Live Data Simulation:** Integrates with the **NHTSA API** to fetch real-world model data.
- **Decoupled Architecture:** Built with a **FastAPI** backend and a lightweight HTML/JS frontend.

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **Backend:** FastAPI, Uvicorn
- **Data Science:** NumPy, Pandas
- **API:** Python Requests, Pydantic

## 📦 How to Run
1. Clone the repo:
```bash
   git clone [https://github.com/YOUR_USERNAME/AutoRank.git](https://github.com/YOUR_USERNAME/AutoRank.git)
```
2. Install dependencies:
```bash
  pip install -r requirements.txt
```
3. Run the server:
```bash
python main.py
```
4. Open http://127.0.0.1:8000 in your browser.
