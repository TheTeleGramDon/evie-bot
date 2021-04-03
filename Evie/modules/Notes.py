from Evie import tbot, CMD_HELP
from Evie.events import register
from Evie.function import can_change_info, is_admin
import os
from telethon.tl import types, functions
from Evie import *
from Evie.modules.sql.notes_sql import add_note, get_all_notes, get_notes, remove_note
from telethon import events

@tbot.on(events.NewMessage(pattern=r"\#(\S+)"))
async def on_note(event):
    name = event.pattern_match.group(1)
    note = get_notes(event.chat_id, name)
    if not note is None:
      message_id = event.sender_id
      if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
    await event.reply(note.reply, reply_to=message_id)

@register(pattern="^/save ?(.*)")
async def _(event):
    if event.is_group:
      if not await is_admin(event, event.sender_id):
        await event.reply("You need to be an admin to do this.")
        return
      if not await can_change_info(message=event):
        await event.reply("You are missing the following rights to use this command:CanChangeInfo")
        return
    else:
        return
    if not event.reply_to_msg_id:
     input = event.pattern_match.group(1)
     if input:
       arg = input.split(" ", 1)
     if len(arg) == 2:
      name = arg[0]
      msg = arg[1]
     else:
      name = arg[0]
      if not name:
        await event.reply("You need to give the note a name!")
        return
      await event.reply("You need to give the note some content!")
      return
    if event.reply_to_msg_id:
     reply_message = await event.get_reply_message()
     msg = reply_message.text
     name = event.pattern_match.group(1)
     if not msg:
        return
     if not name:
        await event.reply("You need to give the note a name!")
        return
    note = msg
    add_note(
            event.chat_id,
            name,
            note,
        )
    await event.reply(f"Saved note `{name}`.")

@register(pattern="^/notes$")
async def on_note_list(event):
    if event.is_group:
        pass
    else:
        return
    all_notes = get_all_notes(event.chat_id)
    OUT_STR = f"List of notes in {event.chat.title}:\n"
    if len(all_notes) > 0:
        for a_note in all_notes:
            OUT_STR += f"- `{a_note.keyword}`\n"
    else:
        OUT_STR = "No notes in {event.chat.title}!"
    OUT_STR += "\nYou can retrieve these notes\nby using `/get notename`, or \n#notename"
    if len(OUT_STR) > 4096:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = "notes.text"
            await tbot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Available notes",
                reply_to=event,
            )
    else:
        await event.reply(OUT_STR)

#Balance Soon