from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
api_id = 29268693
api_hash = "1ad7c3f7c78b8ca2a1888b757764ae03"
bot_token = "6764349911:AAGbdkcXZbzERauGsYXJuwK15RSz3RhECdQ"

app = Client("my_bot", api_id, api_hash, bot_token=bot_token)


@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_photo("https://telegra.ph/file/5c8944fa4bd469d2c7bc2.jpg", caption=f"Hello {message.from_user.first_name}! Welcome to Truecaller Advance",reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Help", callback_data="help")],
        [InlineKeyboardButton("About", callback_data="about")],
    ]))


@app.on_callback_query(filters.regex("help"))
async def help(client, callback_query):
    await callback_query.answer("Here's a list of available commands:", show_alert=True)
    await callback_query.message.edit_text("Here's a list of available commands: \n \n  /trace 8894003445   \n  ", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Help", callback_data="help")],
        [InlineKeyboardButton("About", callback_data="about")],
    ]))


@app.on_callback_query(filters.regex("about"))
async def about(client, callback_query):
    await callback_query.answer("This is a bot made by @xi_xi_xi_xi_xi_xi .", show_alert=True)
    await callback_query.message.edit_text("This is a bot made by @xi_xi_xi_xi_xi_xi.", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Help", callback_data="help")],
        [InlineKeyboardButton("About", callback_data="about")],
    ]))

@app.on_message(filters.command("trace") & filters.private)

async def trace(client, message):

    number = message.text.split()[1]

    try:

        response = requests.get(f"https://phoneapi-4edcc08a9ce5.herokuapp.com/trace/{number}")

        response.raise_for_status()

        result = response.json()

        reply_text = ""

        for key, value in result.items():

            reply_text += f"{key}: {value}\n "

        await message.reply_text(reply_text, quote=True)

    except requests.exceptions.HTTPError as e:

        await message.reply_text(f"Error: {e}")

    except requests.exceptions.ConnectionError:

        await message.reply_text("Error: Could not connect to the API")

    except requests.exceptions.Timeout:

        await message.reply_text("Error: Timeout while connecting to the API")

    except ValueError as e:

        await message.reply_text(f"Error: Invalid JSON response: {e}")





app.run()
