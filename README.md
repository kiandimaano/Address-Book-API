# Address Book API

A RESTful API built with FastAPI and SQLite for managing addresses with coordinate-based distance search.

## Requirements

- Windows OS
- Python 3.8.10
- PowerShell

## Setup

```powershell
git clone <your-repo-url>
cd address-book-api

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# If you get a script execution error, run this once then retry the above:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt

# Create your .env file
Copy-Item .env.example .env
# Or create it manually:
New-Item .env -ItemType File
Add-Content .env "DATABASE_URL=sqlite:///./addresses.db"
```

## Run

```powershell
uvicorn app.main:app --reload
```

---

## Testing the API via Swagger UI

Once the server is running, open your browser and go to: http://localhost:8000/docs

This loads the built-in Swagger UI where you can test every endpoint interactively.

---

### How to use Swagger

For every endpoint below, follow these steps:

1. Click the endpoint to expand it
2. Click **Try it out**
3. Fill in the required fields or request body
4. Click **Execute**
5. Check the **Response body** and **Code** at the bottom

---

### 1. Create an Address — `POST /addresses/`

Click **POST /addresses/**, then **Try it out**. Replace the request body with:

```json
{
  "street": "123 Rizal Ave",
  "city": "Manila",
  "state": "NCR",
  "country": "PH",
  "postal_code": "1000",
  "latitude": 14.5995,
  "longitude": 120.9842
}
```

**Expected:** Response code `201`, returns the created address with an `id` and `created_at`.

---

### 2. List All Addresses — `GET /addresses/`

Click **GET /addresses/**, then **Try it out** → **Execute**.

To test pagination, fill in the query parameters:

| Parameter | Value | Description |
|-----------|-------|-------------|
| `skip` | `0` | Records to skip |
| `limit` | `2` | Records to return |

- `skip=0, limit=2` → Page 1 (first 2 records)
- `skip=2, limit=2` → Page 2 (next 2 records)
- `skip=4, limit=2` → Page 3 (last records)

**Expected:** Returns a paginated response with `total`, `skip`, `limit`, and a `data` array.

---

### 3. Get One Address — `GET /addresses/{address_id}`

Click **GET /addresses/{address_id}**, then **Try it out**. Enter `1` in the `address_id` field.

**Expected:** Returns the address with `id: 1`.

To test a missing record, enter `999` as the `address_id`.

**Expected:** Response code `404` with `"Address not found"`.

---

### 4. Update an Address — `PUT /addresses/{address_id}`

Click **PUT /addresses/{address_id}**, then **Try it out**. Enter `1` in the `address_id` field. Only include the fields you want to change:

```json
{
  "city": "Quezon City"
}
```

**Expected:** Returns the updated address with `city` now showing `Quezon City`.

---

### 5. Search Nearby Addresses — `GET /addresses/nearby/search`

Click **GET /addresses/nearby/search**, then **Try it out**. Fill in the query parameters:

| Parameter | Value |
|-----------|-------|
| `latitude` | `14.5995` |
| `longitude` | `120.9842` |
| `distance_km` | `50` |

**Expected:** Returns all addresses within 50 km of the given coordinates.

---

### 6. Test Validation — `POST /addresses/` with bad data

Click **POST /addresses/**, then **Try it out**. Submit with an invalid latitude:

```json
{
  "street": "Bad St",
  "city": "X",
  "state": "X",
  "country": "X",
  "latitude": 999,
  "longitude": 0
}
```

**Expected:** Response code `422 Unprocessable Entity` with a validation error message about latitude being out of range.

---

### 7. Delete an Address — `DELETE /addresses/{address_id}`

Click **DELETE /addresses/{address_id}**, then **Try it out**. Enter `1` in the `address_id` field.

**Expected:** Response code `204`, no response body.

To confirm deletion, go to **GET /addresses/1** and execute it.

**Expected:** Response code `404` with `"Address not found"`.

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /addresses/ | Create address |
| GET | /addresses/ | List all addresses (supports `skip` and `limit` for pagination) |
| GET | /addresses/{id} | Get one address |
| PUT | /addresses/{id} | Update address |
| DELETE | /addresses/{id} | Delete address |
| GET | /addresses/nearby/search | Find addresses within a given distance |

## Reset Database

```powershell
# Stop the server first (Ctrl+C), then:
Remove-Item addresses.db
uvicorn app.main:app --reload
```

The database is automatically recreated on startup.