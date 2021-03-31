from telethon import events
from Evie import tbot, BOT_ID
from Evie.events import register
from Evie.function import can_change_info

from Evie.modules.sql.welcome_sql import (
    add_welcome_setting,
    get_current_welcome_settings,
    rm_welcome_setting,
    update_previous_welcome,
)
from Evie.modules.sql.welcome_sql import (
    add_goodbye_setting,
    get_current_goodbye_settings,
    rm_goodbye_setting,
    update_previous_goodbye,
)


@tbot.on(events.ChatAction)
async def hi(event):
  if event.user_joined:
   if not event.user_id == BOT_ID:
    cws = get_current_welcome_settings(event.chat_id)
    if cws:
     a_user = await event.get_user()
     chat = await event.get_chat()
     title = chat.title
     count = len(await event.client.get_participants(chat))
     mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)
     first = a_user.first_name
     last = a_user.last_name
     username = (
                f"@{me.username}" if me.username else f"[Me](tg://user?id={me.id})"
            )
     userid = a_user.id
     if last:
         fullname = f"{first} {last}"
     else:
         fullname = first
     current_saved_welcome_message = cws.custom_welcome_message
     current_message = await event.reply(
                    current_saved_welcome_message.format(
                        mention=mention,
                        title=title,
                        count=count,
                        first=first,
                        last=last,
                        fullname=fullname,
                        username=username,
                        userid=userid,
                    ),
                    file=cws.media_file_id,
                )
     update_previous_welcome(event.chat_id, current_message.id)

@register(pattern="^/setwelcome")
async def _(event):
    if event.fwd_from:
        return
    if not await can_change_info(message=event):
        return
    msg = await event.get_reply_message()
    if msg and msg.media:
        tbot_api_file_id = pack_bot_file_id(msg.media)
        add_welcome_setting(event.chat_id, msg.message, False, 0, tbot_api_file_id)
        await event.reply("The new welcome message has been saved!")
    else:
        input_str = event.text.split(None, 1)
        add_welcome_setting(event.chat_id, input_str[1], False, 0, None)
        await event.reply("The new welcome message has been saved!")
