#!pip install python-telegram-bot
# esta ya no funciona bien !pip install goslate 
#!pip install googletrans==4.0.0-rc1 la version 3.0 que se instala por defecto falla
#  from tokenize import String
#  import requests
#  import logging
from cgitb import text
from gc import callbacks
from socket import timeout
from xmlrpc.client import Boolean
from numpy import double
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InlineQuery, ChatAction
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from gpt3 import Gpt3
from googletrans import Translator
import time
from collections import deque

#  logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",level=logging.INFO)
#  INPUT_TEXT = 0

class RMPixel_Bot:

    def __init__(self, token = "5106931346:AAHDYM7jeVfAfRg7tuF-9eXh8Y0ldZgBGo0",ia : Gpt3 = Gpt3()):
        self.token = token
        #  Inicializo conecto con Bot de Telegram.    
        self.ia=ia        
        self.debug = False
        self.translate=False
        self.context_bot()
        self.header_en = "The following is a conversation with a computer AI. The AI is helpful, creative, clear and very friendly" 
        self.context_en = ["HUMAN: Hi! Who are you?",
        "AI: I am an AI who will help you solve your computer questions" ,
        "HUMAN: I have many questions",
        "AI: What do you want to ask me?" 
        ]

        self.header_es = "Lo siguiente es una conversación con una AI. La AI es útil, creativa, clara y muy amigable." 
        self.context_es = ["HUMAN: Hola, ¿Quién eres?",
        "AI: Soy una AI que te ayudará a resolver tus preguntas sobre informática" ,
        "HUMAN: ¿Me puedes contestar siempre en español?",
        "AI: Por supuesto, ¿Qué me quieres preguntar?" 
        ]                  
        
   
    def start_command(self,update: Update, context: CallbackContext):            
       
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                 text="Bienvenido al Bot de RMPixel\n\nEste bot le ayudará a resolver dudas e incluso incidencias relacionadas con la informática.\n\nComience haciendo cualquier consulta o ejecute el comando /help para obtener ayuda\n"
                                 )  
        self.status_command(update,context)
        
    def status_command(self,update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Configuración actual:\nMotor GPT-3: " + self.ia.engine + "\nTemperatura: " + str(self.ia.temperature) + "\nTop_p: " + str(self.ia.top_p) + "\nNúmero máximo de Tokens en respuesta: " + str(self.ia.max_tokens) + "\nTraducción activada: " + str(self.translate) + "\nNúmero de frases de contexto: " + str(self.remembered_context) + "\nNumero de respuestas devueltas por el motor: " + str(self.ia.n) +  "\nModo Debug Activado: " + str(self.debug))    
        if len(self.header_context[0]) > 0:
             context.bot.send_message(chat_id=update.effective_chat.id, text="\nCabecera incluida: \n" + self.header_context[0])                                 
        else:
             context.bot.send_message(chat_id=update.effective_chat.id, text="\nCabecera NO incluida: \n")                                 

        if len(self.context) > 0:
            context_status = list(self.context) # lista con todos el contexto.
            context_status = "\n".join(context_status)  
            context.bot.send_message(chat_id=update.effective_chat.id, text="Contexto actual: \n" + context_status)                                 
        else:
             context.bot.send_message(chat_id=update.effective_chat.id, text="Contexto Vacío: \n")                                 
                                 
                                 

    def end_command(self,update: Update, context: CallbackContext):    
        context.bot.send_message(chat_id=update.effective_chat.id, text="Finalizado Bot @rmpixel_bot. Deberá ser iniciado en el servidor manualmente\n")
        print("Finalizado Bot @rmpixel_bot. Deberá ser iniciado en el servidor manualmente\n")
        self.state=99 # Estado que indica que se quiere terminar la ejecución
        self.updater.stop()

    def restart_command(self,update: Update, context: CallbackContext):    
        context.bot.send_message(chat_id=update.effective_chat.id, text="Reiniciado Bot @rmpixel_bot")
        print("Reiniciado Bot rmpixel_bot, se ha detenido\n\n")
        self.state=-1 # Estado que indica que se quiere reiniciar el bot        
        self.updater.stop()
        

    def temperature_command(self,update: Update, context: CallbackContext):    
        self.ia.temperature = float(context.args[0])        
        print (self.ia.temperature)
        if  self.ia.temperature > 1.0 or self.ia.temperature < 0.0:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Valor de Temperatura debe estar comprendido entre 0 y 1")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Temperatura asignada a: " + str(self.ia.temperature))            
    
    def top_p_command(self,update: Update, context: CallbackContext):    
        self.ia.top_p = float(context.args[0])        
        print (self.ia.top_p)
        if  self.ia.top_p > 1.0 or self.ia.top_p < 0.0:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Valor de Top_p debe estar comprendido entre 0 y 1")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Top_p asignado a: " + str(self.ia.top_p)) 

    def max_tokens_command(self,update: Update, context: CallbackContext):    
        self.ia.max_tokens = int(context.args[0])        
        context.bot.send_message(chat_id=update.effective_chat.id, text="Max_tokens asignado a: " + str(self.ia.temperature))

    def n_command(self,update: Update, context: CallbackContext):    
        self.ia.n = int(context.args[0])        
        context.bot.send_message(chat_id=update.effective_chat.id, text="Parámetro n asignado a: " + str(self.ia.n))


    def translate_command(self,update: Update, context: CallbackContext):    
        self.translate = not self.translate
        context.bot.send_message(chat_id=update.effective_chat.id, text="Traducción interna Español a Inglés <-> Inglés a Español esta ahora: " + str(self.translate) + "\n"
        )        

    def memory_command(self,update: Update, context: CallbackContext):    
        # Como context_bot espera en cabecera un string, y en context una lista,
        # saco el string de la lista y convierto context(que es una cola) en lista
        self.context_bot(int(context.args[0]),list(self.context),self.header_context[0])  
        context.bot.send_message(chat_id=update.effective_chat.id, text="Se ha modificado numero de frases de contexto.\nPuede haber afectado al contexto actual, si el número de frases de contexto es menor al anterior"
        )        

    def debug_command(self,update: Update, context: CallbackContext):    
        self.debug = not self.debug
        context.bot.send_message(chat_id=update.effective_chat.id, text="Modo Depuración está ahora: " + str(self.debug) + "\n"
        )        

    def help_command(self,update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text=
        "Consejo: Para obtener una respuesta lo más correcta posible, debe asegurarse de ser claro tanto en la descripción del problema o duda a consultar, como en la pregunta\n"+
        "Puede recordar este patrón de consulta: Problema + Pregunta asociada \n\n"+        
        "Listado de comandos disponibles\n"+
        "\nComandos generales:\n"+
        "/help       :  Muestra esta ayuda\n"+
        "/start      :  Mensaje introductorio al manejo del bot\n"+
        "/restart    :  Reinicia el estado del Bot a un estado limpio.(el contexto, basado en preguntas y respuestas anteriores se pierde)\n"+
        "/end        :  Finaliza la ejecución del Bot. Deberá ser iniciado manualmente en el servidor\n"+
        "/debug      :  Activa o desactiva el modo Debug\n"+
        "/status     :  Muestra la configuración actual\n\n" +
        "\nComandos exclusimos para el motor GPT-3:\n" +
        "/temperature:  Especifica lo aleatorio de las respuestas. Rango(0 preciso - 1 más aleatorio) \n"+
        "/top_p      :  Alternativa a la temperatura. Indica el porcentaje de respuestas con mayor puntuación considerados Rango (0 - 1) \n"+
        "/n          :  Número de respuestas devueltas por el motor. Permite a mi algoritmo seleccionar la mejor. ¡Ojo!, consume más tokens\n"+
        "/max_tokens :  Número máximo de tokens en las respuestas\n"+
        "/translate  :  Activa o desactiva la autotraducción ES-EN <-> EN-ES\n"+
        "/memory     :  Cantidad de frases de contexto a enviar junto con la pregunta y cabecera si se incluye"
        "\nComando de configuración global y gráfica:\n" +
        "/config     :  Opciones de configuración\n" 

        )
        
    def unknown_command(self,update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Lo siento, no entendí su comando.\n\n")
        self.help_command(update,context)

    def callback_selected_context(self, update: Update, context: CallbackContext ):          
        context.bot.answer_callback_query(callback_query_id=update.callback_query.id)
        query =  update.callback_query 
        context.bot.answer_callback_query(callback_query_id=update.callback_query.id)
        query =  update.callback_query 

        button_header_ia_spanish = InlineKeyboardButton(
            text="Cabecera Informática Inglés",
            callback_data="selected_header_english"
        )
        button_header_ia_english = InlineKeyboardButton(
            text="Cabecera Informática Español",
            callback_data="selected_header_spanish"
        )
        button_header_empty = InlineKeyboardButton(
            text="Sin cabecera",
            callback_data="selected_header_empty"
        )
        query.edit_message_text(text="Opciones de configuración para contexto Inicial: ",
                                reply_markup=InlineKeyboardMarkup([[button_header_ia_english,button_header_ia_spanish],[button_header_empty]])
                                )       


    def select_sentences_context(self, update: Update, context: CallbackContext ):
        button_sentences_spanish = InlineKeyboardButton(
            text="Frases Informática Español",
            callback_data="selected_sentences_spanish"
        )
        button_sentences_english = InlineKeyboardButton(
            text="Frases Informática Inglés",
            callback_data="selected_sentences_english"
        )
        button_sentences_empty = InlineKeyboardButton(
            text="Sin Frases de contenxo",
            callback_data="selected_sentences_empty"
        )        
        context.bot.send_message(chat_id=update.effective_chat.id, text="¿Seleccione frases de contexto que desea Utilizar?",
                                reply_markup=InlineKeyboardMarkup([[button_sentences_spanish, button_sentences_english],[button_sentences_empty]]))           

    def context_seted(self, update: Update, context: CallbackContext):  
        self.context_bot(6,self.context_tmp,self.header_context_tmp)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Se ha eliminado todo el contexto anterior.\nSe ha configurado nuevo contexto con memoria para las 6 últimas frases.\nUtilize /memory para reducir o ampliar el número de frases de contexto.\n")
                                


    def callback_selected_sentences_english(self, update: Update, context: CallbackContext ):  
        context.bot.answer_callback_query(callback_query_id=update.callback_query.id)
        query =  update.callback_query         
        self.context_tmp = self.context_en
        self.context_seted(update,context)
        query.edit_message_text(text="Seleccionada Frases Informática en Inglés.")             

    def callback_selected_sentences_spanish(self, update: Update, context: CallbackContext ):  
        context.bot.answer_callback_query(callback_query_id=update.callback_query.id)
        query =  update.callback_query         
        self.context_tmp = self.context_es
        self.context_seted(update,context)
        query.edit_message_text(text="Seleccionada Frases Informática en Español.")             

    def callback_selected_sentences_empty(self, update: Update, context: CallbackContext ):  
        context.bot.answer_callback_query(callback_query_id=update.callback_query.id)
        query =  update.callback_query         
        self.context_tmp = []
        self.context_seted(update,context)
        query.edit_message_text(text="No se enviarán frases de contexto al motor.")             


    def callback_selected_header_english(self, update: Update, context: CallbackContext ):  
        context.bot.answer_callback_query(callback_query_id=update.callback_query.id)
        query =  update.callback_query         
        self.header_context_tmp = self.header_en
        query.edit_message_text(text="Seleccionada Cabecera Informática en Inglés.")     
        self.select_sentences_context(update,context)
        
    def callback_selected_header_spanish(self, update: Update, context: CallbackContext ):  
        context.bot.answer_callback_query(callback_query_id=update.callback_query.id)
        query =  update.callback_query         
        self.header_context_tmp = self.header_es
        query.edit_message_text(text="Seleccionada Cabecera Informática en Español.")     
        self.select_sentences_context(update,context)
    
    def callback_selected_header_empty(self, update: Update, context: CallbackContext ):  
        context.bot.answer_callback_query(callback_query_id=update.callback_query.id)
        query =  update.callback_query         
        self.header_context_tmp = ""
        query.edit_message_text(text="No se enviará ninguna cabecera.")     
        self.select_sentences_context(update,context)
    
    def callback_selected_gpt3(self, update: Update, context: CallbackContext ):          
        context.bot.answer_callback_query(callback_query_id=update.callback_query.id)
        query =  update.callback_query 

        button_translate = InlineKeyboardButton(
            text="Activar Traducción ES-EN",
            callback_data="selected_translate"
        )
        button_engine = InlineKeyboardButton(
            text="Seleccionar Motor",
            callback_data="selected_engine"
        )
        button_context = InlineKeyboardButton(
            text="Seleccionar Contexto Inicial",
            callback_data="selected_context"
        )
        query.edit_message_text(text="Opciones de configuración GPT-3: ",
                                reply_markup=InlineKeyboardMarkup([[button_engine,button_translate],[button_context]])
                                )        
    
    def callback_selected_training(self, update: Update, context: CallbackContext ):          
        context.bot.answer_callback_query(callback_query_id=update.callback_query.id)
        query =  update.callback_query 

        button_finetunning = InlineKeyboardButton(
            text="Fine Tunning",
            callback_data="select_finetunning"
        )
        button_query_answer = InlineKeyboardButton(
            text="Modo Preguntas/Respuestas",
            callback_data="select_query_answer"
        )
        button_train = InlineKeyboardButton(
            text="Crear train.jsonl",
            callback_data="select_train"
        )
        query.edit_message_text(text="Entrenamiento Base de Conocimiento: ",
                                reply_markup=InlineKeyboardMarkup([[button_train],[button_finetunning,button_query_answer]])
                                )        

    def callback_selected_translate(self, update: Update, context: CallbackContext ):  
        context.bot.answer_callback_query(callback_query_id=update.callback_query.id)
        query =  update.callback_query         
        self.translate = not self.translate
        query.edit_message_text(text="Traducción interna Español a Inglés <-> Inglés a Español esta ahora: " + str(self.translate) + "\n")        

    def callback_selected_engine1(self, update: Update, context: CallbackContext ):  
        context.bot.answer_callback_query(callback_query_id=update.callback_query.id)
        query =  update.callback_query 
        self.ia.engine ="text-davinci-002"
        query.edit_message_text(text="Seleccionado Motor: " + self.ia.engine + "\n")        

    def callback_selected_engine2(self, update: Update, context: CallbackContext ):  
        context.bot.answer_callback_query(callback_query_id=update.callback_query.id)
        query =  update.callback_query         
        self.ia.engine ="text-curie-001"
        query.edit_message_text(text="Seleccionado Motor: " + self.ia.engine + "\n")        

    def callback_selected_engine3(self, update: Update, context: CallbackContext ):  
        context.bot.answer_callback_query(callback_query_id=update.callback_query.id)
        query =  update.callback_query                 
        self.ia.engine ="text-babbage-001"
        query.edit_message_text(text="Seleccionado Motor: " + self.ia.engine + "\n")        

    def callback_selected_engine4(self, update: Update, context: CallbackContext ):  
        context.bot.answer_callback_query(callback_query_id=update.callback_query.id)
        query =  update.callback_query         
        self.ia.engine ="text-ada-001"
        query.edit_message_text(text="Seleccionado Motor: " + self.ia.engine + "\n")        
    
    def callback_selected_engine5(self, update: Update, context: CallbackContext ):  
        context.bot.answer_callback_query(callback_query_id=update.callback_query.id)
        query =  update.callback_query         
        self.ia.engine ="davinci"
        query.edit_message_text(text="Seleccionado Motor: " + self.ia.engine + "\n")       

    def callback_selected_engine6(self, update: Update, context: CallbackContext ):  
        context.bot.answer_callback_query(callback_query_id=update.callback_query.id)
        query =  update.callback_query         
        self.ia.engine ="curie"
        query.edit_message_text(text="Seleccionado Motor: " + self.ia.engine + "\n")       

    def callback_selected_engine7(self, update: Update, context: CallbackContext ):  
        context.bot.answer_callback_query(callback_query_id=update.callback_query.id)
        query =  update.callback_query         
        self.ia.engine ="babbage"
        query.edit_message_text(text="Seleccionado Motor: " + self.ia.engine + "\n")       

    def callback_selected_engine8(self, update: Update, context: CallbackContext ):  
        context.bot.answer_callback_query(callback_query_id=update.callback_query.id)
        query =  update.callback_query         
        self.ia.engine ="ada"
        query.edit_message_text(text="Seleccionado Motor: " + self.ia.engine + "\n")       

    def callback_selected_engine(self, update: Update, context: CallbackContext ):   

        context.bot.answer_callback_query(callback_query_id=update.callback_query.id)
        query =  update.callback_query 

        button_engine1 = InlineKeyboardButton(
            text="text-davinci-002",
            callback_data="text-davinci-002"
        )
        button_engine2 = InlineKeyboardButton(
            text="text-curie-001",
            callback_data="text-curie-001"
        )

        button_engine3 = InlineKeyboardButton(
            text="text-babbage-001",
            callback_data="text-babbage-001"
        )

        button_engine4 = InlineKeyboardButton(
            text="text-ada-001",
            callback_data="text-ada-001"
        )

        button_engine5 = InlineKeyboardButton(
            text="davinci",
            callback_data="davinci"
        )

        button_engine6 = InlineKeyboardButton(
            text="curie",
            callback_data="curie"
        )
        button_engine7 = InlineKeyboardButton(
            text="babbage",
            callback_data="babbage"
        )
        button_engine8 = InlineKeyboardButton(
            text="ada",
            callback_data="ada"
        )


        query.edit_message_text(text="El motor actual es: "+ self.ia.engine + "\nSelecciona el nuevo Motor deseado",reply_markup=InlineKeyboardMarkup([[button_engine1,button_engine5],[button_engine2,button_engine6],[button_engine3,button_engine7],[button_engine4,button_engine8]]))        
        
        
    def config_command(self, update: Update, context: CallbackContext):
                
        button_web = InlineKeyboardButton(
            text="Visitar nuestra web",
            url ="http://prueba.rmpcorreo.com"
        )
        button_gpt3 = InlineKeyboardButton(
            text="GPT-3",
            callback_data="selected_GPT-3"
        )
        button_training = InlineKeyboardButton(
            text="Training",
            callback_data="selected_training"
        )
        
        context.bot.send_message(chat_id=update.effective_chat.id, text="¿Seleccione la opción que desea configurar?",reply_markup=InlineKeyboardMarkup([[button_web],[button_gpt3,button_training]]))

    """
    Método callback, para la conversación
    """
    def conversation(self, update:Update, context: CallbackContext):      
        context.bot.send_chat_action(chat_id=update.effective_chat.id,action=ChatAction.TYPING)        
        
        #  Preparo prompt a enviar, en base al contexto a recordar          

        if self.translate: # se actualiza el contexto con el texto ya traducido.
            translator =  Translator()
            text_trans= translator.translate(update.message.text,dest='en').text            

            if self.remembered_context > 0:
                text = "HUMAN: " + text_trans + "\nAI:"
                if len(self.context) >= self.remembered_context:            
                    #Extraigo el elemento más antiguo e inserto el nuevo.
                    self.context.popleft() 

                self.context.append(text)
                query = self.header_context + list(self.context) # lista con todos el contexto.
                query = "\n".join(query)  
                response, response_full = self.ia.prompt(query)
            else:
                query = self.header_context
                query = "\n".join(query) +  text_trans                  
                response, response_full = self.ia.prompt(query)

            if self.debug:
                print ("\nContexto para obtener la respuesta:\n" + query) 
                context.bot.send_message(chat_id=update.effective_chat.id, text="\nContexto para obtener la respuesta:\n" + query)
                print ("\nRespuesta Completa GPT-3: \n" + str(response_full))
                context.bot.send_message(chat_id=update.effective_chat.id, text="\nRespuesta Completa GPT-3:\n" + str(response_full))            
                context.bot.send_message(chat_id=update.effective_chat.id, text="\nRespuesta Obtenida tras procesamiento:\n")

            response_trans = translator.translate(response, dest='es').text
            context.bot.send_message(chat_id=update.effective_chat.id, text=response_trans)            
            if self.remembered_context > 0:
                response = "AI:" + response
                text = "HUMAN: " + text_trans
                self.context.pop()
                self.context.append(text) # aqui inserto en la cola el verdadero texto, para que no se rompa la estructura HUMANO: AI:

            if self.remembered_context > 0:
                if len(self.context) >= self.remembered_context:            
                    #Extraigo el elemento más antiguo e inserto el nuevo.
                    self.context.popleft()

                self.context.append(response)

        else:        
            if self.remembered_context > 0:
                text = "HUMAN: " + update.message.text + "\nAI:"            
                if  len(self.context) >= self.remembered_context:            
            #   Extraigo el elemento más antiguo e inserto el nuevo.
                    self.context.popleft()

                self.context.append(text)                                       
                query = self.header_context + list(self.context) # lista con todos el contexto.
                query = "\n".join(query)            
                response,response_full = self.ia.prompt(query) 
            else:
                query = self.header_context
                query = "\n".join(query)  + update.message.text                  
                response, response_full = self.ia.prompt(query)
            if self.debug:            
                print ("\nContexto para obtener la respuesta:\n" + query) 
                context.bot.send_message(chat_id=update.effective_chat.id, text="\nContexto para obtener la respuesta:\n" + query)
                print ("\nRespuesta Completa GPT-3: \n" + str(response_full))
                context.bot.send_message(chat_id=update.effective_chat.id, text="\nRespuesta Completa GPT-3:\n" + str(response_full))            
                context.bot.send_message(chat_id=update.effective_chat.id, text="\nRespuesta Obtenida tras procesamiento:\n")

            context.bot.send_message(chat_id=update.effective_chat.id, text=response)            

            if self.remembered_context > 0:
                response = "AI:" + response            
                text = "HUMAN: " + update.message.text
                self.context.pop()     
                self.context.append(text) # aqui inserto en la cola el verdadero texto, para que no se rompa la estructura HUMANO: AI:

                if len(self.context) >= self.remembered_context:            
                #Extraigo el elemento más antiguo e inserto el nuevo.
                    self.context.popleft()

                self.context.append(response)            

            
                

    def start_bot(self,drop_pending_updates = False):        
        self.state = 0        
        #  Inicio el Bot
        self.updater = Updater(self.token, use_context =True)
        self.dp = self.updater.dispatcher        
        #  Agrego los handlers básicos
        self.dp.add_handler(CommandHandler("start",self.start_command))
        self.dp.add_handler(CommandHandler("help",self.help_command))
        self.dp.add_handler(CommandHandler("restart",self.restart_command))
        self.dp.add_handler(CommandHandler("end",self.end_command))
        self.dp.add_handler(CommandHandler("status",self.status_command))
        self.dp.add_handler(CommandHandler("debug",self.debug_command))
        self.dp.add_handler(CommandHandler("temperature",self.temperature_command))
        self.dp.add_handler(CommandHandler("top_p",self.top_p_command))
        self.dp.add_handler(CommandHandler("n",self.n_command))
        self.dp.add_handler(CommandHandler("max_tokens",self.max_tokens_command))
        self.dp.add_handler(CommandHandler("memory",self.memory_command))
        self.dp.add_handler(CommandHandler("translate",self.translate_command))
        self.dp.add_handler(CommandHandler("config",self.config_command))
        
        self.dp.add_handler(CallbackQueryHandler(pattern="selected_engine",callback=self.callback_selected_engine))
        self.dp.add_handler(CallbackQueryHandler(pattern="text-davinci-002",callback=self.callback_selected_engine1))
        self.dp.add_handler(CallbackQueryHandler(pattern="text-curie-001",callback=self.callback_selected_engine2))
        self.dp.add_handler(CallbackQueryHandler(pattern="text-babbage-001",callback=self.callback_selected_engine3))
        self.dp.add_handler(CallbackQueryHandler(pattern="text-ada-001",callback=self.callback_selected_engine4))        
        self.dp.add_handler(CallbackQueryHandler(pattern="davinci",callback=self.callback_selected_engine5))
        self.dp.add_handler(CallbackQueryHandler(pattern="curie",callback=self.callback_selected_engine6))
        self.dp.add_handler(CallbackQueryHandler(pattern="babbage",callback=self.callback_selected_engine7))
        self.dp.add_handler(CallbackQueryHandler(pattern="ada",callback=self.callback_selected_engine8))
        self.dp.add_handler(CallbackQueryHandler(pattern="selected_GPT-3",callback=self.callback_selected_gpt3))
        self.dp.add_handler(CallbackQueryHandler(pattern="selected_training",callback=self.callback_selected_training))
        self.dp.add_handler(CallbackQueryHandler(pattern="selected_translate",callback=self.callback_selected_translate))
        self.dp.add_handler(CallbackQueryHandler(pattern="selected_context",callback=self.callback_selected_context))
        self.dp.add_handler(CallbackQueryHandler(pattern="selected_sentences_spanish",callback=self.callback_selected_sentences_spanish))
        self.dp.add_handler(CallbackQueryHandler(pattern="selected_sentences_english",callback=self.callback_selected_sentences_english))
        self.dp.add_handler(CallbackQueryHandler(pattern="selected_sentences_empty",callback=self.callback_selected_sentences_empty))
        self.dp.add_handler(CallbackQueryHandler(pattern="selected_header_spanish",callback=self.callback_selected_header_spanish))      
        self.dp.add_handler(CallbackQueryHandler(pattern="selected_header_english",callback=self.callback_selected_header_english))
        self.dp.add_handler(CallbackQueryHandler(pattern="selected_header_empty",callback=self.callback_selected_header_empty))
                
        

        self.dp.add_handler(MessageHandler(Filters.command,self.unknown_command))
        self.dp.add_handler(MessageHandler(Filters.text,self.conversation))
        
        
        self.updater.start_polling(drop_pending_updates=drop_pending_updates) #  Inicio el bot
        print("Iniciado Bot RMPixel. Esperando consultas...\n\n")
        return 

    #  permite definir una cabecera y contexto. Este contexto
    def context_bot( self,remembered_context = 0, context : list = [], header_context: str = "") :
        """ La cabecera, se utilizará siempre y se enviará antes que las frases de contexto.
            
            El contexto incluirá las frases, que contendrá el prompt inicial, y que hará de contexto a la pregunta.
            Este contexto se irá modificando, quedando solo el número de entradas en la lista que indique remembered_context.
            El conteto debe tener siempre una pregunta/respuesta precedida de Humano: o AI: 
            
            Ejemplo(cada frase será un string y ocupará una posición un una lista que se transformará en una cola):
            "HUMANO: Hola, ¿Como estás?"
            "AI: Estoy bien, ¿de que quieres hablar?"

            Nota: No hace falta poner los \n, puesto que cada entrada ya se considerará una frase nueva. y se agregará automáticamente.
            
            Durante la conversación con el Bot, se agregará automáticamente la palabra AI y HUMANO, según corresponda.
            De forma transparente al usuario
        """
        self.context = deque(context,maxlen=remembered_context)            
        self.remembered_context = remembered_context
        self.header_context = [header_context] # convierto el string a lista para despues poderlo fusionar fácilmente con la self.context convertido a lista.
        


