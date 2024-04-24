from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bs4 import BeautifulSoup
import requests
import re
from pyrogram.types import Message
from config import api_id, api_hash, bot_token


app = Client("my_bot", api_id, api_hash, bot_token=bot_token)


# Define a filter to check if the user is in the channel or group
def check_user_in_channel(func):

  async def wrapper(_, message: Message):
    # Replace 'YOUR_CHANNEL_ID' with the ID of your channel or group
    channel_id = -100123456789  # Example channel ID
    user_id = message.from_user.id
    try:
      # Check if the user is in the channel
      await app.get_chat_member(channel_id, user_id)
      # User is found, allow them to use commands
      await func(_, message)
    except Exception as e:
      # User is not found, reply with a message asking them to join first
      await message.reply_text("Please join our channel or group first.")

  return wrapper


@app.on_message(filters.new_chat_members)
async def welcome_message(client, message):
  for member in message.new_chat_members:
    # Send a private message to the new member
    await client.send_message(
        chat_id=member.id,
        text="Welcome to my bot",
    )
    await client.send_message(
        chat_id=member.id,
        text=
        "how to use this BOT \n \n **इस रोबोट का उपयोग कैसे करें**, \n \n send your number without country number  "
    )


@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
  await app.delete_bot_commands()
  channel_id = -1001967606455  # Example channel ID
  user_id = message.from_user.id
  try:
    await app.get_chat_member(channel_id, user_id)
    await message.reply_photo(
        "https://telegra.ph/file/5c8944fa4bd469d2c7bc2.jpg",
        caption=
        f"Hello {message.from_user.first_name}! Welcome to Truecaller Advance",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Help", callback_data="help")],
            [InlineKeyboardButton("About", callback_data="about")],
            [InlineKeyboardButton("Join Channel FOR MORE BOTS", url="https://t.me/Xi_BOTS")],
        ]))
  except Exception as e:
    abtbtn = InlineKeyboardMarkup([[
        InlineKeyboardButton("JOIN CHANNEL FOR UPDATES", url="https://t.me/+Y9O5ptuPEFs3NGE1")
    ]])
    await message.reply_text(
        "Please join our channel or group first. Then CLICK ON BUTTON RESTART ",
        reply_markup=abtbtn)


@app.on_callback_query(filters.regex("help"))
async def help(client, callback_query):
  await callback_query.answer("Here's a list of available commands:",
                              show_alert=True)
  await callback_query.message.edit_text(
      "Here's a list of available commands: \n \n \n    \n \n  send your 10 digit number 8894003445   \n  ",
      reply_markup=InlineKeyboardMarkup([
          [InlineKeyboardButton("Help", callback_data="help")],
          [InlineKeyboardButton("About", callback_data="about")],
          [InlineKeyboardButton("Join Channel FOR MORE BOTS", url="https://t.me/Xi_BOTS")],
      ]))


def get_number_details(number):
  data = f"country=IN&q={number}"
  headers = {
      'Content-Type':
      'application/x-www-form-urlencoded',
      'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.71 Safari/537.36'
  }
  try:
    response = requests.post('https://calltracer.in/',
                             headers=headers,
                             data=data)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    tableData = {}
    for row in soup.select('.trace-details tr'):
      cols = row.find_all('td')
      if len(cols) == 2:
        key = cols[0].text.strip()
        value = cols[1].text.strip()
        tableData[key] = value
    return tableData  # Just return tableData directly
  except requests.RequestException as e:
    return {"error": str(e)}

@app.on_message(filters.text & filters.regex(r'\b\d{10}\b'))
async def number_handler(client, message):
    await app.delete_bot_commands()  # Assuming you want to clear default bot commands; place outside try block
    number = message.text.strip()

    try:
        if re.fullmatch(r'\d{10}', number):
            details = get_number_details(number)
            # Format the details in a pretty "key: value" string format
            details_message = '\n'.join([f'{key}: {value}' for key, value in details.items()])
            await message.reply_text(details_message)
    except Exception as e:  # Catch exceptions related to fetching or formatting number details
        abtbtn = InlineKeyboardMarkup([
            [InlineKeyboardButton("JOIN CHANNEL FOR UPDATES", url="https://t.me/+Y9O5ptuPEFs3NGE1")]
        ])
        await message.reply_text(
            "An error occurred or you need to join our channel to use this. Click below to join:",
            reply_markup=abtbtn
        )
@app.on_callback_query(filters.regex("about"))
async def about(client, callback_query):
  await callback_query.answer("This is a bot made by @xi_xi_xi_xi_xi_xi .",
                              show_alert=True)
  await callback_query.message.edit_text(
      "This is a bot made by @xi_xi_xi_xi_xi_xi.",
      reply_markup=InlineKeyboardMarkup([
          [InlineKeyboardButton("Help", callback_data="Help")],
          [InlineKeyboardButton("Join Channel FOR MORE BOTS", url="https://t.me/Xi_BOTS")],
          [InlineKeyboardButton("About", callback_data="About")],
      ]))


app.run()
            
