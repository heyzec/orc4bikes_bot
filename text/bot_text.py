HELP_TEXT = """
🏦 /topup - Top up to use the bot now!
🗾 /routes - orc4bikes-curated routes
ℹ️ /status - Credits and rental status
📜 /history - Recent 10 transactions
✨ /fun - Interesting..

Rental rates:
3 credits per minute

🚲 /bikes - See available bikes
🚴 /rent - Start your rental trip here!
🔓 /getpin - Get the PIN for the bike you rented
↩️ /return - End your rental trip here!
📢 /report - Report damages or anything sus
✍️ /feedback - A penny for your thoughts, for all our past events!

Top-up:
$1 = 100 credits
"""

# Telegram MarkdownV2
ADMIN_TEXT = r"""*Admin menu*
__User commands__
/user `USERNAME` \- View the user's current status
/addcredit `USERNAME` `AMOUNT` \- Top up the user's credit by an integer amount
/deduct `USERNAME` `AMOUNT` \- Deduct the user's credit by an integer amount
/setcredit `USERNAME` `AMOUNT` \- Set the user's credit to an integer amount
/ban `USERNAME` \- Ban a selected user
/unban `USERNAME` \- Unban a selected user

__Bikes commands__
/orcabikes \- Get all bikes and their current status
/setpin `BIKENAME` `NEWPIN` \- Change the bike's pin in the server to a new pin
/setstatus `BIKENAME` `NEWSTATUS` \- Change the bike's status in the server to a new status
/forcereturn `BIKENAME` \- Forcefully return a selected bike

__Other commands__
/logs \- Get rental and report logs as a csv file

_Quicktip: Press and hold command to get it pretyped on your keyboard\!_
"""

START_MESSAGE = "Please /start me privately to access this service!"


FUN_TEXT = """
Feel free to click any of the below, or just send /random...
🐶 /doggo - Get a random dog!
🐕 /shibe - Get a random shiba!
🐈 /neko - Get a random cat!
🐱 /kitty - Get a random kitten!
🦊 /foxy - Get a random fox!
🐥 /birb - Get a random bird!
🐹 /pika - A wild pikachu appeared!

Look out for more easter eggs 🥚... :)
"""

BAN_MESSAGE = """You are on Santa's naughty list... What have you done?!
If you believe this is a mistake, contact the ORC4BIKES Head at @{ADMIN_HEAD}"""

# HTML
TERMS_TEXT = """<b>Bicycle Rental -- Terms of Use</b>
1. You are not to HOG the bike.
2. You must take GOOD CARE of the bike during the duration of rental.
3. If you spot any DEFECTS, /report before your rental. Any defects found after your rental will be your responsibility.
4. You will be FINANCIALLY held liable for any DAMAGES to the bike, and/or LOSS of equipment on the bike.
5. orc4bikes reserve the right to amend the 'Terms of Use' at their discretion.
6. You agree to take good care of YOURSELF and follow proper safety procedures.

In case of emergencies, call ambulance 995, and inform either
 - {ADMIN_HEAD_NAME} at <code>{ADMIN_HEAD_MOBILE}</code> @{ADMIN_HEAD} - ORC4BIKES Head, or
 - {ADMIN_SAFETY_NAME} at <code>{ADMIN_SAFETY_MOBILE}</code> @{ADMIN_SAFETY} - ORC4BIKES Safety

If you agree, and ONLY if you agree, to the terms stated above, click "Accept".
"""

RENTAL_RENT_TEMPLATE = """[RENTAL - RENT]
@{username} rented {bike_name} at {time}."""

RENTAL_RETURN_TEMPLATE = """[RENTAL - RETURN]
@{username} returned {bike_name} at {time}."""

FINANCE_PAYMENT_TEMPLATE = """[FINANCE - PAYMENT]
@{username} paid ${amt} at {time}."""

REPORT_TEMPLATE = """[REPORT]
@{username} sent the following report:
{desc}"""
