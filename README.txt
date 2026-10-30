This is a basic dummy authentication API service that just validated the predetermined dummy credentials.

Start the service harness to launch the monitor, primary, and passive warm standby:

python main.py

The monitor automatically promotes the standby after three failed status checks.
Failover logs include timestamps for [Crash Detected], [Failover Triggered], and [Service Restored].

Session state is checkpointed to auth_checkpoint.json after successful logins.

Run the local failover test with:

python test_failover.py

Test credentials are:
1. admin:password123
2. user:password

Test curl command:
curl -X POST http://localhost:5555/login -H "Content-Type: application/json" -d '{"username":"admin","password":"password123"}'
