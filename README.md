# Secret Santa Assignment

This project generates Secret Santa assignments based on employee lists and previous assignments. The user uploads two CSV files:

1. **Employee List CSV**: Contains details about employees (name, email).
2. **Previous Assignments CSV**: Contains details of previous Secret Santa pairings to avoid repeat pairings.

The backend (Flask) processes these files, ensuring valid assignments and sends the result as a downloadable CSV file.

## Features

- Upload employee list and previous assignments.
- Automatically generates new Secret Santa assignments, avoiding previous pairings.
- Download a CSV file with the new assignments.
  
## Requirements

- **Python 3.10**
- **Flask**: Web framework to handle API requests.
- **Flask-CORS**: This is for cross-origin resource sharing (if the front and back end are on different domains).

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/secret-santa-assignment.git
cd secret-santa-assignment
```
### 2. Install dependencies
```base
pip install -r requirements.txt
```
### 3. Running the Backend (Flask API)
```base
python app.py
```
### 4. Running the Frontend
 - You can open the **index.html** file in any browser. 
 - If you're running the frontend and backend on different servers, ensure the backend allows cross-origin requests (CORS), as configured with Flask-CORS.
