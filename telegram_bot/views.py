import telebot
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from config.settings import BOT_TOKEN
from .bot import bot


@csrf_exempt
def web_hook(request):
    if request.headers.get('content-type') == 'application/json':
        
        json_string = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        print(update)
        try:
            bot.process_new_updates([update])
        except:
            print(traceback.format_exc())
        
        return JsonResponse({'ok': True})
    else:
        return JsonResponse({'ok': False})