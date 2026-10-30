'''

1. Ticket summary. Create variables for one ticket:

ticket_id, title, priority (an int from 1 to 4)
hours_open (a float), is_resolved (a bool), assigned_to (set to None)

Print the type of each. Then print a one-line summary with an f-string, with hours to one decimal place:

Ticket 1042: VPN not connecting | P2 | open 5.5h

'''

ticket_id = 1042
title = "VPN not connecting"
priority = 2
hours_open = 5.5
is_resolved = False
assigned_to = None

print(type(ticket_id))     # <class 'int'>
print(type(title))         # <class 'str'>
print(type(priority))      # <class 'int'>
print(type(hours_open))    # <class 'float'>
print(type(is_resolved))   # <class 'bool'>
print(type(assigned_to))   # <class 'NoneType'>

print(f"Ticket {ticket_id}: {title} | P{priority} | open {hours_open:.1f}h")



'''

2. SLA check. Using if/elif/else:

Set sla_hours by priority: P1 = 4, P2 = 8, P3 = 24, anything else = 72.
If hours_open is over the SLA, print BREACHED. Otherwise print how many hours are left, for example Within SLA: 2.5h left.
Separately, if assigned_to is None, print Unassigned.

'''

if priority == 1:
    sla_hours = 4
elif priority == 2:
    sla_hours = 8
elif priority == 3:
    sla_hours = 24
else:
    sla_hours = 72

if hours_open > sla_hours:
    print("BREACHED")
else:
    print(f"Within SLA: {sla_hours - hours_open:.1f}h left")

if assigned_to is None:
    print("Unassigned")


'''

3. Count breaches. You have the hours open for five P2 tickets:

python
hours_list = [2, 9.5, 30, 1, 8.0]

Loop through them, print each one with BREACHED or OK, then print the total number breached. That’s the loop version of SELECT COUNT(*) … WHERE hours > 8. Think about whether 8.0 exactly counts as a breach, and make your code match what you decide.

'''

hours_list = [2, 9.5, 30, 1, 8.0]
sla_hours = 8
breached = 0

for hours in hours_list:
    if hours > sla_hours:
        print(f"{hours}h: BREACHED")
        breached += 1
    else:
        print(f"{hours}h: OK")

print(f"{breached} of {len(hours_list)} breached")

'''

4. Input validation. Use input("Enter priority (1-4): ") to ask for a priority, and keep asking in a while loop until the input is valid. Two hints:

input() always returns a string.
"3".isdigit() returns True.

Once the input is valid, print the SLA hours for that priority.

'''

while True:
    user_input = input("Enter priority (1-4): ")
    if user_input.isdigit() and 1 <= int(user_input) <= 4:
        priority = int(user_input)
        break
    print("Invalid input. Please enter a number between 1 and 4.")

if priority == 1:
    sla_hours = 4
elif priority == 2:
    sla_hours = 8
elif priority == 3:
    sla_hours = 24
else:
    sla_hours = 72

print(f"SLA hours for P{priority}: {sla_hours}")