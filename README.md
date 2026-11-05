\# Python Microservice



A Python-based microservice application built using FastAPI. It provides Weather, Joke, and Text Summary APIs with API key authentication, input validation, error handling, and automated testing.



\## Features



\- Weather API using Open-Meteo

\- Joke API using an external joke provider

\- Text Summary API with local mock mode and optional OpenAI integration

\- API key authentication

\- Request validation and error handling

\- Asynchronous API operations

\- Automated tests using Pytest

\- Interactive API documentation using Swagger UI



\## Tech Stack



\- Python 3.14

\- FastAPI

\- Uvicorn

\- HTTPX

\- Pydantic

\- OpenAI Python SDK (optional)

\- Pytest

\- Pytest-Asyncio



\## Project Structure



```text

python-microservice/

├── app/

│   ├── core/

│   ├── routers/

│   ├── schemas/

│   ├── services/

│   ├── main.py

│   └── dependencies.py

├── tests/

├── .env.example

├── .gitignore

├── requirements.txt

├── Dockerfile

├── docker-compose.yml

└── README.md

```



\## Installation



Clone the repository:



```bash

git clone YOUR\_GITHUB\_REPOSITORY\_URL

cd python-microservice

```



Create a virtual environment:



```bash

python -m venv venv

```



Activate on Windows PowerShell:



```powershell

venv\\Scripts\\Activate.ps1

```



Install dependencies:



```bash

pip install -r requirements.txt

```



\## Environment Configuration



Create a `.env` file in the project root.



Configure the following variables:



```env

APP\_NAME=Python Microservice

APP\_ENV=development

DEBUG=True

API\_KEY=your-local-api-key

OPENAI\_API\_KEY=

OPENAI\_MODEL=gpt-4.1-mini

MAX\_TEXT\_LENGTH=10000

USE\_MOCK\_LLM=True

```



Never upload your actual `.env` file or API keys to GitHub.



\## Run the Application



```bash

python -m uvicorn app.main:app --reload

```



Application URL:



http://127.0.0.1:8000



Swagger API documentation:



http://127.0.0.1:8000/docs



\## API Endpoints



| Method | Endpoint | Description |

|---|---|---|

| GET | `/` | Application status |

| GET | `/weather?city=Pune` | Weather information |

| GET | `/joke` | Random joke |

| POST | `/summary` | Text summary |



The Summary API requires the `X-API-Key` request header.



Example request:



```json

{

&#x20; "text": "Python is a popular programming language. It is used in web development and AI."

}

```



\## Run Tests



```bash

python -m pytest tests/ -v

```



\## Current Test Status



8 automated tests passed during development.



\## License



This project is available for learning and demonstration purposes.

