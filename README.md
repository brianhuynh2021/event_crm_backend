python -m app.main

## 🧪 Example API Usage

### Filter users by company and city
...

### Filter users by hosted and attended count with pagination and sorting

curl -X GET "http://127.0.0.1:8000/api/v1/users/filter?attended_min=2" -H "accept: application/json"

curl -X GET "http://127.0.0.1:8000/api/v1/users/filter?hosted_min=1&hosted_max=5&attended_min=0&attended_max=3&sort_by=created_at&sort_dir=desc&skip=0&limit=10" -H "accept: application/json"
