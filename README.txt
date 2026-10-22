This is a basic dummy authentication API service that just validated the predetermined dummy credentials.

Test credentials are:
1. admin:password123
2. user:password

Test curl command:
curl -X POST http://localhost:5555/login -H "Content-Type: application/json" -d '{"username":"admin","password":"password123"}'
