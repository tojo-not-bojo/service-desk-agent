import os
from dotenv import load_dotenv

load_dotenv()                      # reads .env and loads its values into the environment
print(os.getenv("TEST_SECRET"))    # fetches one value by name
