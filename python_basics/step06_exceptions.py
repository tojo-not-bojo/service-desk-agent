from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


'''
Read a traceback. Add this code and run it. Which line failed, what’s the exception, and what does the message tell you?
python
   TICKETS_BY_ID = {1044: {"title": "Wi-Fi drops in office"}}

   def get_title(ticket_id):
       return TICKETS_BY_ID[ticket_id]["title"]

   print(get_title(9999))

Then delete it, or comment it out, so it doesn’t stop the rest of the file.
'''
TICKETS_BY_ID = {1044: {"title": "Wi-Fi drops in office"}}

def get_title(ticket_id):
    return TICKETS_BY_ID[ticket_id]["title"]

print(get_title(9999))
'''
A safer load_json. Rewrite load_json from step 5 so that:
a missing file raises FileNotFoundError with a message giving the full path and suggesting running step05_export.py
invalid JSON raises ValueError with the file name and the line where the problem is (a json.JSONDecodeError has .lineno and .msg attributes)
Create data/broken.json containing {"id": 1, "title": "Broken",}. The trailing comma is invalid JSON. Test with "missing.json" and "broken.json", catching each error so the script prints the message instead of crashing.
'''

'''
parse_priority(value) -> int. It should accept values like 2 and " 3 " and return the int. For anything that isn’t a whole number from 1 to 4, raise ValueError with a clear message. Test it with 2, " 3 ", "abc", 7, None and 2.5.
'''

'''
A tool that doesn’t crash. Update get_ticket_status (load the tickets with load_json) so it also accepts IDs given as strings, like "1044". For anything that isn’t a number, return an error dict instead of crashing. Test it with 1044, "1044", "abc" and 9999.
'''

'''
Keep a batch going. Process this list with parse_priority. Collect the valid priorities and the error messages, without stopping at the first failure. Use try/except/else, then print a summary.
python
   raw_values = [1, "2", "high", 4, None, " 3 ", 9]
'''


