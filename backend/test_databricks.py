print("TEST 1 - Python is running")

from database.databricks import test_connection

print("TEST 2 - Databricks module imported")

result = test_connection()

print("TEST 3 - Connection successful")
print("Users in Databricks:", result)