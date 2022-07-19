import asyncio
import base64
import json

import pyaudio
import websockets

# Import API funcs and Key for AssemblyAI
from api_secrets import AA_API_KEY as auth_key
from contact_manager import *
from media_data import get_trending_media
from news_data import get_news
from open_ai import ask_computer
from tts import speak
from weather_data import get_weather
from send_messages import send_email, send_text

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()
 
# Start Recording
stream = p.open(
   format=FORMAT,
   channels=CHANNELS,
   rate=RATE,
   input=True,
   frames_per_buffer=FRAMES_PER_BUFFER
)
 
# Assembly AI Endpoint
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"
 
# Asynchronous function for websocket
async def send_receive():
   async with websockets.connect(
       URL,
       extra_headers=(("Authorization", auth_key),),
       ping_interval=None,
       ping_timeout=80,
       close_timeout=60
   ) as _ws:
       await asyncio.sleep(0.1)
       print("Receiving SessionBegins ...")
       session_begins = await _ws.recv()
       print(session_begins)
       print("Sending messages ...")
       async def send():
           while True:
               try:
                # Do not throw exception on overflow i.e. if internet is too slow
                   data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
                   data = base64.b64encode(data).decode("utf-8")
                   json_data = json.dumps({"audio_data":str(data)})
                   await _ws.send(json_data)
               except websockets.exceptions.ConnectionClosedError as e:
                   print(e)
                   assert e.code == 4008
                   break
               except Exception as e:
                   assert False, "Not a websocket 4008 error"
               await asyncio.sleep(0.01)
          
           return True
      
       async def receive():
           while True:
               try:
                   result_str = await _ws.recv()
                   json_data = json.loads(result_str)
                   prompt = json_data['text']
                   # Check if message is complete
                   if prompt and json_data['message_type'] == 'FinalTranscript':
                        print(f'Me: {prompt}\n')
                        lowered_prompt = prompt.lower().rstrip('.')
                        # Check prompt for keywords to access APIs
                        if 'weather' in lowered_prompt:
                            response = get_weather()
                        elif 'movie' in lowered_prompt or 'tv' in lowered_prompt:
                            response = get_trending_media(prompt)
                        elif 'news' in lowered_prompt:
                            response = get_news(lowered_prompt)
                        elif ('text' in lowered_prompt or 'message' in lowered_prompt) and 'to' in lowered_prompt:
                            send_text(lowered_prompt)
                        elif 'email' in lowered_prompt and 'to' in lowered_prompt:
                            send_email(lowered_prompt)
                        elif 'contact' in lowered_prompt:
                            if 'add' in lowered_prompt or 'create'in lowered_prompt or 'insert' in lowered_prompt:
                                add_contact()
                            elif 'update' in lowered_prompt or 'alter' in lowered_prompt or 'edit' in lowered_prompt:
                                update_contact()
                            elif 'delete' in lowered_prompt or 'remove' in lowered_prompt:
                                delete_contact()
                            continue
                        # Ask user to specify who they would like to message
                        elif 'text' in lowered_prompt:
                            speak("Please specify who you would like to text")
                        elif 'email' in lowered_prompt:
                            speak("Please specify who you would like to email")
                        else:
                            response = ask_computer(prompt)
                        print(f'Computer: {response.lstrip()}\n')
                        speak(response)

               except websockets.exceptions.ConnectionClosedError as e:
                   assert e.code == 4008
                   break
               except Exception as e:
                   print("Terminating Session")
                   quit()

      
       send_result, receive_result = await asyncio.gather(send(), receive())

asyncio.run(send_receive())
