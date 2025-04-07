# Project Setup Guide  

## 1. Create a Virtual Environment  
Run the following command to create a virtual environment:  
```sh
python -m venv .venv
```

## 2. Activate the Virtual Environment  
- **On macOS/Linux:**  
  ```sh
  source .venv/bin/activate
  ```
- **On Windows (Command Prompt):**  
  ```sh
  .venv\Scripts\activate
  ```
- **On Windows (PowerShell):**  
  ```sh
  .venv\Scripts\Activate.ps1
  ```

## 3. Upgrade pip  
Ensure you have the latest version of `pip`:  
```sh
python -m pip install --upgrade pip
```

## 4. Install Dependencies  
Install FastAPI and its required dependencies:  
```sh.venv\Scripts\activate.venv\Scripts\activate
pip install "fastapi[standard]"
```

## 5. Run the Project  
Start the FastAPI application using Uvicorn:  
```sh
uvicorn main:app --reload
```

## 6. Access the API  
Once the server is running, you can access:  
- API: [http://127.0.0.1:8000](http://127.0.0.1:8000)  
- Interactive Docs (Swagger UI): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
