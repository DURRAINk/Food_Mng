# 🍽️ Food Wastage Management System

A secure, scalable, and professionally branded Streamlit app for tracking and managing food inventory, expiry dates, and wastage metrics. Built with a robust SQL backend, modular CRUD operations, and role-based access control for collaborative deployment.

---

## 🚀 Features

- ✅ **Streamlit Dashboard** with branded UI and background image
- ✅ **SQL Integration** with least-privilege roles and audit logging
- ✅ **Modular CRUD Operations** with session state and deduplication
- ✅ **Expiry Tracking** and visualizations using custom palettes
- ✅ **Role-Based Access** for safe collaboration and data integrity
- ✅ **Responsive Layout** with top-level titles and professional styling

---

## 🛠️ Tech Stack

| Layer        | Tools Used                          |
|--------------|-------------------------------------|
| Frontend     | Streamlit, HTML/CSS, custom theming |
| Backend      | SQL Server                          |
| Visualization| Streamlit APIs                      |
| Deployment   | Streamlit Cloud                     |

---
## To use visit : 
https://food-management-system-by-durraink.streamlit.app/

## To develop:
### 📦 Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/DURRAINk/Food_Mng.git
   cd Food_Mng
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
3. **Run app.py**
---
3. **Storing data**
   * The data is already stored in the `food_management.db` file.
   * If you want to use your own sql server:
        ```bash
        pip install pyodbc   #for MSSQL
        pip install pymysql   #for MYSQL
   1. Creating the database in your server
   2. In `database.py` replace:
        ```bash
        "sqlite:///food_management.db"
   to
        
   
        "mssql+pyodbc://user:pass@host/db?driver=ODBC+Driver+17+for+SQL+Server"  #for MSSQL

        "mysql+pymysql://username:password@host:port/database_name" #for MYSQL
        
   4. **Run app.py**
