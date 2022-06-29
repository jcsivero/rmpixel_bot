import sys
import os
from RMPixel_Telegram import RMPixel_Bot

if __name__ == "__main__":
   bot = RMPixel_Bot()       
   bot.start_bot(drop_pending_updates=True)
   #bot.ia.delete_all_files()
   #print (bot.ia.list_files())
   #input()

   #bot.ia.delete_all_ft()
   #print (bot.ia.list_files())
   #print (bot.ia.list_ft())
   #bot.ia.my_ft_model()
   #bot.ia.openai.Model.delete("ft-wqRjAyJqAkJvkiW9BPYChzue")
   #bot.ia.openai.FineTune.cancel(id="ft-wqRjAyJqAkJvkiW9BPYChzue")
   #print (bot.ia.list_ft())
   #input()
   #bot.ia.openai.FineTune.list_events(bot.ia.list_ft()[0]["id"])
   #bot.ia.openai.FineTune.list_events(id="ft-wqRjAyJqAkJvkiW9BPYChzue")
   
   

while bot.state != 99: #  99 indica valor para detener definitivamente el bot
    while  bot.updater.running:
        pass
    if bot.state == -1:
        bot.start_bot(drop_pending_updates=False)                    

print ("Finalizado BOT RMPixel")
sys.exit()
