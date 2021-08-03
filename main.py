from telethon import TelegramClient, events
from google_drive_ocr.application import GoogleOCRApplication
import os


api_id = 12345 #Your Id
api_hash = '123456789sdfghjkl45t' #Your Hash
app = GoogleOCRApplication('cred.json') #Your Google Drive API
channelusername = 'youridchannel'
client = TelegramClient('bots', api_id, api_hash) #Your Session name
@client.on(events.NewMessage())
async def handler(event):
    if event.message.raw_text == '/start':
        await event.respond('Welcome to bot')
    if event.message.raw_text == '/help':
        await event.respond('This is Help Text')
    joinstatus = True
    entity = await client.get_entity(channelusername)
    members = await client.get_participants(entity)
    for member in members:
        if member.id == event.sender_id:
            joinstatus = False
            if event.photo is not None or event.message.document is not None:
                if event.photo or event.message.document.mime_type == 'image/jpeg' or event.message.document.mime_type == 'image/png':
                    saved_path = await event.download_media()
                    print(saved_path)
                    await event.respond('Processing!')
                    
                    if(app.perform_ocr(saved_path)):
                        f = open(app.get_output_path(saved_path),mode="r", encoding="utf-8")
                        try:
                            await event.respond(f.read())
                            f.close()
                        except:
                            await event.respond('We dont make find your text in this image')
                        if os.path.exists(saved_path) and os.path.exists(app.get_output_path(saved_path)) :
                            os.remove(saved_path)
                            os.remove(app.get_output_path(saved_path))
                else:
                    await event.respond('Please send Image')
    if joinstatus == True:
        await event.respond('Please join channel to use this bot\nid:'+channelusername)
        
client.start()
client.run_until_disconnected()
