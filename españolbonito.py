# -*- coding: utf-8 -*-

# This is a simple Hello World Alexa Skill, built using
# the implementation of handler classes approach in skill builder.
import logging
import boto3
import json
import random

from random import randint

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_dynamodb.adapter import DynamoDbAdapter


from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response
from ask_sdk_model.interfaces.alexa.presentation.apl import (
    RenderDocumentDirective, ExecuteCommandsDirective, SpeakItemCommand,
    AutoPageCommand, HighlightMode)

dataMap ={
    "welcome_0": "Bienvenido a Español Bonito, ¿Que te parece si empezamos con una lección de entrenemiento?, recuerda que también puedes pedirme ayuda.",

    "welcome_1": "Español Bonito está aquí para mejorar el idioma que hablamos, ¿quieres empezar la lección hoy?",

    "welcome_2": "Empieza a mejorar tu español con un entrenamiento rápido. ¿Empezamos?",
    #Frases de la intencion RecordsIntent
    "logrosinicio1": "La práctica hace al maestro.",


    "logros": "Tú estás en el nivel {{ level }}, tú puntaje general en Bla Bla es de {{ score }}, y tu última medalla alcanzada ha sido {{ badge }}",

    "logroscierre1": "¡Sigue así! de seguro todavía puedes con otra lección.",

    "logroscierre2": "¿Has intentado leer 15 minutos al día? ¡Eso podría ayudarte a mejorar!",

    "logroscierre3": "¡Felicidades!",


    #Frases de la intencion ExamIntent
    "exam": "Empecemos con la evaluación",
    #Frases de la intencion DailyChallengeIntent

    "dc": "Empecemos con el reto diario",
    #Frases de la intencion TrainingIntent

    "training_0": "Empieza el entrenamiento ¡Mucho éxito!",

    "training_1": "A entrenar",

    "training_2": "Dale, estamos para mejorar",

    #Frases de la intencion AMAZON.HelpIntent
    "ayuda_0": "Te ayudaré un poco en como usar la skill. Puedes pedirme un entrenemiento para poder mejorar en lenguas, si te sientes lo suficientemente preparado puedes hacer una evaluación para acceder a un nivel más retante. También puedes preguntarme por tus logros para saber cuales son los últimos que has logrado. Y si te sientes aventurero, puedes hacer el reto diario para mejorar tú idioma. ¿Con qué empezamos?",

    "ayuda_1": "Puedo hacer muchas cosas. Puedes pedirme un entrenemiento para poder mejorar en lenguas, si te sientes lo suficientemente preparado puedes hacer una evaluación para acceder a un nivel más retante. También puedes preguntarme por tus logros para saber cuales son los últimos que has logrado. Y si te sientes aventurero, puedes hacer el reto diario para mejorar tú idioma. ¿Qué te gustaría hacer?",

    "ayuda_2": "No te preocupes, yo te explicaré que hacer. Puedes pedirme un entrenemiento para poder mejorar en lenguas, si te sientes lo suficientemente preparado puedes hacer una evaluación para acceder a un nivel más retante. También puedes preguntarme por tus logros para saber cuales son los últimos que has logrado. Y si te sientes aventurero, puedes hacer el reto diario para mejorar tú idioma. ¿Cúal quisieras explorar?",

    "goodbye": "Que tengas un buen día.",


    #Frases de la intencion RecordsIntent
    "logrosinicio1": "La práctica hace al maestro.",

    "logrosinicio2": "",

    "logrosinicio3":"",

    "logrosinicio4":"",

    "logrosinicio5":"",


    "logros": "Tú estás en el nivel {{ level }}, tú puntaje general en Bla Bla es de {{ score }}, y tu última medalla alcanzado ha sido {{ badge }}.",
    #Frases TriviaIntent
    "triviasucces_0":"elegiste la respuesta correcta",

    "triviasucces_1":"Muy bien, sigue así",

    "triviasucces_2":"Respuesta correcta",

    "triviasucces_3":"Acertaste",

    "triviasucces_4":"Bien, lo has logrado",

    "triviasucces_5":"Esa es la respuesta",

    "triviasucces_6":"elegiste la respuesta correcta",

    "triviafail_0":"Esa no es, intenta con la siguiente",

    "triviafail_1":"Uy, parece que te has equivocado",

    "triviafail_2":"Error, intentemos con otra",

    "triviafail_3":"No es correcto",

    "triviafail_4":"Fallaste, te recuperas en la siguiente",

    #Frases de la intencion ExamIntent

    #Frases de la intencion DailyChallengeIntent

    #Frases de la intencion TrainingIntent

    #Frases de la intencion AMAZON.HelpIntent

    "ayuda1": "No te preocupes, yo te explicaré que hacer. Puedes pedirme un entrenemiento para poder mejorar en lenguas, si te sientes lo suficientemente preparado puedes hacer una evaluación para acceder a un nivel más retante. También puedes preguntarme por tus logros para saber cuales son los últimos que has logrado. Y si te sientes aventurero, puedes hacer el reto diario para mejorar tú idioma.",


    ## PREGUNTAS ###


}
questions={
    1: [
      {
        "id": "1",
        "pregunta": "¿cuál de estos animales se escribe con v?",
        "opc1": "vaca",
        "opc2": "caballo",
        "opc3": "búfalo",
        "answer":"búfalo"
      },
      {
        "id": "2",
        "pregunta": "¿cuál de estas palabras se escribe con z?",
        "opc1": "Serpiente",
        "opc2": "Saltamontes",
        "opc3": "Pez",
        "answer":"Pez"
      },
      {
        "id": "3",
        "pregunta": "¿cúal de estas palabras llevan dieresis?",
        "opc1": "Pingüíno",
        "opc2": "Búho",
        "opc3": "Iguana",
        "answer": "Pingüíno"
      },
      {
        "id": "4",
        "pregunta": "¿cúal de estos animales se escribre con b?",
        "opc1": "Oveja",
        "opc2": "Abeja",
        "opc3": "Venado",
        "answer": "Abeja"
      },
      {
        "id": "5",
        "pregunta": "¿cuál de estos animales su nombre es una palabra esdrujula?",
        "opc1": "Murciélago",
        "opc2": "Cacatúa",
        "opc3": "Caimán",
        "answer":"Murciélago"
      },
      {
        "id": "6",
        "pregunta": "¿cuál de estos colores lleva tilde?",
        "opc1": "Cian",
        "opc2": "Carmesí",
        "opc3": "Zafiro",
        "answer":"Carmesí"
      },
      {
        "id": "7",
        "pregunta": "¿cuál de estos colores lleva la letra z?",
        "opc1": "Azul",
        "opc2": "Siena",
        "opc3": "turquesa",
        "answer":"Azul"
      },
      {
        "id": "8",
        "pregunta": "¿cuál de estos colores es una palabra aguda?",
        "opc1": "ámbar",
        "opc2": "purpúra",
        "opc3": "marrón",
        "answer":"marrón"
      }
      ],
    2: [
      {
        "id": "1",
        "pregunta": "¿cuál de estos oficios es una palabra esdrujula?",
        "opc1": "Informático",
        "opc2": "Matemático",
        "opc3": "astrólogo",
        "answer":"astrólogo"
      },
      {
        "id": "2",
        "pregunta": "¿cuál de estas profesiones se escribe con la letra v?",
        "opc1": "directivo",
        "opc2": "bioquímico",
        "opc3": "Abogado",
        "answer":"directivo"
      },
      {
         "id": "3",
        "pregunta": "¿cuál de estos oficios llevan tilde?",
        "opc1": "químico",
        "opc2": "arquitecto",
        "opc3": "capturista",
        "answer":"químico"
      },
      {
        "id": "4",
        "pregunta": "¿cuál de estos oficios llevan tilde?",
        "opc1": "químico",
        "opc2": "arquitecto",
        "opc3": "capturista",
        "answer":"químico"
      },
      {
        "id": "5",
        "pregunta": "¿cuál de estas profesiones son agudas?",
        "opc1": "cosmólogo",
        "opc2": "Ecólogo",
        "opc3": "comadrón",
        "answer":"comadrón"
      },
      {
        "id": "6",
        "pregunta": "¿cuál de estas verduras se escribe con z?",
        "opc1": "cebolla",
        "opc2": "zanahoria",
        "opc3": "calabacín",
        "answer":"zanahoria"
      },
      {
         "id": "7",
        "pregunta": "¿cuál de estos alimentos se escribre con c?",
        "opc1": "cilantro",
        "opc2": "pizza",
        "opc3": "setas",
        "answer":"cilantro"
      },
      {
        "id": "8",
        "pregunta": "¿cuál de estos alimentos es una palabra esdrujula?",
        "opc1": "sandía",
        "opc2": "limón",
        "opc3": "azúcar",
        "answer":"azúcar"
      },
      {
        "id": "9",
        "pregunta": "¿cuál de estos alimentos inician con la letra h?",
        "opc1": "uvas",
        "opc2": "huevos",
        "opc3": "obleas",
        "answer":"huevos"
      },
      {
        "id": "10",
        "pregunta": "¿cuál de estos alimentos lleva tilde?",
        "opc1": "lentejas",
        "opc2": "maizena",
        "opc3": "té",
        "answer":"té"
      }
    ],
    3:[
      {
        "id": "1",
        "pregunta": "¿cuál de estos objetos lleva la palabra z?",
        "opc1": "calcetín",
        "opc2": "zapato",
        "opc3": "sandalia",
        "answer":"zapato"
      },
      {
        "id": "2",
        "pregunta": "¿cuál de los siguientes objetos es una palabra esdrujula?",
        "opc1": "calzón",
        "opc2": "teléfono",
        "opc3": "café",
        "answer":"teléfono"
      },
      {
        "id": "3",
        "pregunta": "¿cuál de los siguientes objetos es una palabra grave?",
        "opc1": "brócoli",
        "opc2": "dólar",
        "opc3": "botón",
        "answer":"dólar"
      },
      {
        "id": "4",
        "pregunta": "¿cuál de los siguientes objetos es una palabra aguda?",
        "opc1": "comida",
        "opc2": "cerámica",
        "opc3": "avión",
        "answer":"avión"
      },
      {
        "id": "5",
        "pregunta": "¿cuál de los siguientes objetos no se escriben con h?",
        "opc1": "zanahoria",
        "opc2": "habría",
        "opc3": "asta",
        "answer":"asta"
      },
      {
         "id": "6",
        "pregunta": "¿cuál de las siguientes palabras llevan tilde?",
        "opc1": "tacón",
        "opc2": "pantunflas",
        "opc3": "calcetines",
        "answer":"calcetines"
      },
      {
         "id": "7",
        "pregunta": "¿cuál de las siguientes prendas son palabras agudas?",
        "opc1": "suéter",
        "opc2": "pantalón",
        "opc3": "mezclilla",
        "answer":"pantalón"
      },
      {
         "id": "8",
        "pregunta": "¿cuál de las siguientes prendas llevan la letra s?",
        "opc1": "calcetín",
        "opc2": "cinturón",
        "opc3": "blusa",
        "answer":"blusa"
      },
      {
        "id": "9",
        "pregunta": "¿cuál de las siguientes prendas se escribe con la letra v?",
        "opc1": "botas",
        "opc2": "vestido",
        "opc3": "billetera",
        "answer":"vestido"
      },
      {
        "id": "10",
        "pregunta": "¿cuál de las siguientes prendas se escribe con s?",
        "opc1": "short",
        "opc2": "chamarra",
        "opc3": "chaqueta",
        "answer":"short"
      }
    ],
    4:[
      {
        "id": "1",
        "pregunta": "¿cuál de las siguientes países se escribe con la letra q?",
        "opc1": "kenia",
        "opc2": "pakistán",
        "opc3": "qatar",
        "answer":"qatar"
      },
      {
        "id": "2",
        "pregunta": "¿cuál de las siguientes ciudades llevan tilde?",
        "opc1": "parís",
        "opc2": "barcelona",
        "opc3": "ibiza",
        "answer":"parís"
      },
      {
        "id": "3",
        "pregunta": "¿cuál de las siguientes estados llevan la letra y?",
        "opc1": "nayarit",
        "opc2": "tamaulipas",
        "opc3": "washington",
        "answer":"nayarit"
      },
      {
        "id": "4",
        "pregunta": "¿cuál de los siguientes ciudades son esdrujulas?",
        "opc1": "praga",
        "opc2": "canadá",
        "opc3": "méxico",
        "answer":"méxico"
      },
      {
        "id": "5",
        "pregunta": "¿cuál de las siguientes ciudades son agudas?",
        "opc1": "Inglaterra",
        "opc2": "mónaco",
        "opc3": "irán",
        "answer":"irán"
      },
      {
        "id": "6",
        "pregunta": "¿cuál de las siguientes ciudades son graves?",
        "opc1": "quito",
        "opc2": "camerún",
        "opc3": "bélgica",
        "answer":"quito"
      },
      {
         "id": "7",
        "pregunta": "¿cuál de las siguientes ciudades llevan la letra z?",
        "opc1": "zimbaue",
        "opc2": "senegal",
        "opc3": "sudán",
        "answer":"zimbaue"
      },
      {
         "id": "8",
        "pregunta": "¿cuál de los siguientes paises no llevan h?",
        "opc1": "bahamas",
        "opc2": "holanda",
        "opc3": "irlanda",
        "answer":"irlanda"
      },
      {
        "id": "9",
        "pregunta": "Mi amigo es de Argentina, por lo tanto él es...",
        "opc1": "argentinos",
        "opc2": "argentina",
        "opc3": "argentino",
        "answer":"argentino"
      },
      {
       "id": "10",
        "pregunta": "Caifanes son un grupo de México, por lo tanto ellos son...",
        "opc1": "mexicana",
        "opc2": "mexicas",
        "opc3": "mexicanos",
        "answer":"mexicanos"
      }
      ],
    5:[
        {
         "id": "1",
        "pregunta": "¿cuál de estos libros corresponde de divulgación científica?",
        "opc1": "historia del tiempo",
        "opc2": "el abismo",
        "opc3": "plano americano",
        "answer":"historia del tiempo"
        },
        {
          "id": "2",
        "pregunta": "¿cuál de estos libros es periodistico?",
        "opc1": "frutos extraños",
        "opc2": "sopita de fideo",
        "opc3": "origen de las especies",
        "answer":"frutos extraños"
        },
        {
          "id": "3",
        "pregunta": "¿cuál es una característica de un refrán?",
        "opc1": "contiene varias estrofas",
        "opc2": "armonia",
        "opc3": "fácil de memorizar",
        "answer":"fácil de memorizar"
        },
        {
          "id": "4",
        "pregunta": "¿cuál es una característica de una canción?",
        "opc1": "lenguaje sencillo",
        "opc2": "melodia",
        "opc3": "corto",
        "answer":"melodia"
        },
        {
          "id": "5",
        "pregunta": "¿cuál es una característica de los poemas?",
        "opc1": "rimas",
        "opc2": "ritmo",
        "opc3": "son breves",
        "answer":"rimas"
        },
        {
          "id": "6",
        "pregunta": "¿qué composición literaria contiene una moraleja?",
        "opc1": "cuentos",
        "opc2": "leyendas",
        "opc3": "fabulas",
        "answer":"fabulas"
        },
        {
          "id": "7",
        "pregunta": "¿cuáles son las narraciones que pasan de generación en generación?",
        "opc1": "leyendas",
        "opc2": "mitos",
        "opc3": "fabulas",
        "answer":"leyendas"
        },
        {
          "id": "8",
        "pregunta": "¿cuál de los siguientes relatos son protagonizados por seres sobrenaturales?",
        "opc1": "mitos",
        "opc2": "leyendas",
        "opc3": "cuentos",
        "answer":"mitos"
        },
        {
          "id": "9",
        "pregunta": "¿cuál conocimiento radica en la argumentación validada?",
        "opc1": "religioso",
        "opc2": "directo",
        "opc3": "científico",
        "answer":"científico"
        },
        {
          "id": "10",
        "pregunta": "¿cuál es el conocimiento que se basa en las experiencias de una persona?",
        "opc1": "científico",
        "opc2": "empiríco",
        "opc3": "filosófico",
        "answer":"empiríco"
        }
        ],
    6:[
        {
        "id": "1",
        "pregunta": "¿cuál de las siguientes palabras lleva dieresis?",
        "opc1": "guiso",
        "opc2": "lingüística",
        "opc3": "guillotina",
        "answer":"lingüística"
        },
        {
        "id": "2",
        "pregunta": "¿cuál de estas palabras es un diptongo?",
        "opc1": "viudo",
        "opc2": "buey",
        "opc3": "uruguay",
        "answer":"viudo"
        },
        {
        "id": "3",
        "pregunta": "¿cuál de las siguientes palabras corresponde a la interpretación del dolor?",
        "opc1": "ahí",
        "opc2": "hay (con h)",
        "opc3": "ay (sin h)",
        "answer":"ay (sin h)"
        },
        {
        "id": "4",
        "pregunta": "¿cuál es el tipo de palabras que no se escriben igual pero si se pronuncian igual?",
        "opc1": "homófonas",
        "opc2": "homónimas",
        "opc3": "polisemia",
        "answer":"homófonas"
        },
        {
        "id": "5",
        "pregunta": "¿Cómo se llaman las palabras que tienen distintos significados?",
        "opc1": "polisemia",
        "opc2": "semántica",
        "opc3": "homónimas",
        "answer":"polisemia"
        },
        {
        "id": "6",
        "pregunta": "¿comó se llama a la función sintáctica de unir palabras?",
        "opc1": "verbo",
        "opc2": "nexo",
        "opc3": "sintaxis",
        "answer":"nexo"
        },
        {
        "id": "7",
        "pregunta": "¿cómo se le conoce a el punto en su máximo esplendor?",
        "opc1": "climax",
        "opc2": "contexto",
        "opc3": "desarrollo",
        "answer":"climax"
        },
        {
        "id": "8",
        "pregunta": "¿cuál es el principio por el cual se conectan las palabras entre sí?",
        "opc1": "coherencia",
        "opc2": "cohesión",
        "opc3": "conectividad",
        "answer":"cohesión"
        },
        {
        "id": "9",
        "pregunta": "¿cómo se les conoce a la manera de explicar con nuestras palabras lo que se entendió de un texto?",
        "opc1": "tésis",
        "opc2": "hipotésis",
        "opc3": "paráfrasis",
        "answer":"paráfrasis"
        }
        ]
}



sb = SkillBuilder()

answerSlotKey="AnswerSlot"
level= 2
score=109
triviaQuestions=random.sample(range(8), 4)
triviaScore=0
question={}

print questions[level][triviaQuestions.pop()]['answer']
print triviaQuestions
adapter = DynamoDbAdapter('BonitaSkill', partition_key_name="id",
            attribute_name="attributes", create_table=False,
            partition_keygen="customerid",
            dynamodb_resource=boto3.resource("dynamodb"))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        global answerSlotKey
        global level
        global score
        global triviaQuestions
        global triviaScore
        global question
        global randOption
        # type: (HandlerInput) -> Response
        triviaQuestions=random.sample(range(8), 4)

        speech_text = dataMap['welcome_{}'.format(randOption(3))]

        handler_input.response_builder.speak(speech_text).set_should_end_session(
            False).add_directive(
            RenderDocumentDirective(
                document=_load_apl_document("main.json"),
                datasources={
                "bodyTemplate7Data": {
                    "type": "object",
                    "objectId": "bt7Sample",
                    "title": "",
                    "backgroundImage": {
                        "sources": [
                            {
                                "url": "https://drive.google.com/uc?id=1mcleo4bhLM9XXdK2YGc5J_Y9zNL-4uD4",
                                "size": "small",
                                "widthPixels": 0,
                                "heightPixels": 0
                            },
                            {
                                "url": "https://drive.google.com/uc?id=1mcleo4bhLM9XXdK2YGc5J_Y9zNL-4uD4",
                                "size": "large",
                                "widthPixels": 0,
                                "heightPixels": 0
                            }
                        ]
                    },
                    "image": {
                        "sources": [
                            {
                                "url": "",
                                "size": "small",
                                "widthPixels": 0,
                                "heightPixels": 0
                            },
                            {
                                "url": "",
                                "size": "large",
                                "widthPixels": 0,
                                "heightPixels": 0
                            }
                        ]
                    },
                    "logoUrl": "",
                    "hintText": "Try, \"Alexa, search for blue cheese\""
                }
            }
            )
        )

        return handler_input.response_builder.response

class TrainingIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("TrainingIntent")(handler_input)
    def handle(self, handler_input):
        global answerSlotKey
        global level
        global score
        global triviaQuestions
        global triviaScore
        global question
        global randOption
        # type: (HandlerInput) -> Response
        speech_text = dataMap['training_{}'.format(randOption(3))]
        question = questions[level][triviaQuestions.pop()]
        speech_text = speech_text + " " + question['pregunta'] + " " + question['opc1'] + " " + question['opc2'] + " " + question['opc3']
        handler_input.response_builder.speak(speech_text).set_should_end_session(
            False).add_directive(
            RenderDocumentDirective(
                document=_load_apl_document("training.json"),
                datasources={
                "bodyTemplate1Data": {
                    "type": "object",
                    "objectId": "bt1Sample",
                    "backgroundImage": {
                        "sources": [
                            {
                                "url": "https://drive.google.com/uc?id=1uNrZTtxPwyGV8eAXRFpaqW99kZunkDvS",
                                "size": "small",
                                "widthPixels": 0,
                                "heightPixels": 0
                            },
                            {
                                "url": "https://drive.google.com/uc?id=1uNrZTtxPwyGV8eAXRFpaqW99kZunkDvS",
                                "size": "large",
                                "widthPixels": 0,
                                "heightPixels": 0
                            }
                        ]
                    },
                    "title": "",
                    "textContent": {
                        "primaryText": {
                            "type": "PlainText",
                            "text": ""
                        }
                    },
                    "logoUrl": "https://drive.google.com/uc?id=1uNrZTtxPwyGV8eAXRFpaqW99kZunkDvS"
                }
            }
            )
        )
        return handler_input.response_builder.response

class TriviaIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("TriviaIntent")(handler_input)
    def handle(self, handler_input):
        global answerSlotKey
        global level
        global score
        global triviaQuestions
        global triviaScore
        global question
        global randOption
        useranswer="pollo"
        # type: (HandlerInput) -> Response
        if len(triviaQuestions)==4:
            speech_text = dataMap['training_{}'.format(randOption(3))]
            question = questions[level][triviaQuestions.pop()]
            speech_text = speech_text + " " + question['pregunta'] + " " + question['opc1'] + " " + question['opc2'] + " " + question['opc3']
            handler_input.response_builder.ask("¿Cual es la correcta")
        elif len(triviaQuestions)!=0:
            if answerSlotKey in handler_input.attributes_manager.session_attributes:
                useranswer = handler_input.attributes_manager.session_attributes[answerSlotKey]
            if question['answer'] == useranswer:
                speech_text = dataMap['triviasucces_{}'.format(randOption(6))]
                triviaScore=triviaScore+1
            else:
                speech_text = dataMap['triviafail_{}'.format(randOption(4))]
            question = questions[level][triviaQuestions.pop()]
            speech_text = speech_text + " " + question['pregunta'] + " " + question['opc1'] + " " + question['opc2'] + " " + question['opc3']
            print 'question answer %s' + question['answer']
            print 'user answer %s'+ useranswer
            handler_input.response_builder.ask("¿Cual es la correcta")
        else:
            if answerSlotKey in handler_input.attributes_manager.session_attributes:
                useranswer = handler_input.attributes_manager.session_attributes[answerSlotKey]
            if question['answer'] == useranswer:
                triviaScore=triviaScore+1
            print 'question answer %s' + question['answer']
            print 'user answer %s'+ useranswer
            speech_text = "El entrenamiento ha terminado, haz conseguido " + str(triviaScore) + " puntos"
            triviaScore=0



        handler_input.response_builder.speak(speech_text).set_should_end_session(
            False).add_directive(
            RenderDocumentDirective(
                document=_load_apl_document("training.json"),
                datasources={
                "bodyTemplate1Data": {
                    "type": "object",
                    "objectId": "bt1Sample",
                    "backgroundImage": {
                        "sources": [
                            {
                                "url": "https://drive.google.com/uc?id=1uNrZTtxPwyGV8eAXRFpaqW99kZunkDvS",
                                "size": "small",
                                "widthPixels": 0,
                                "heightPixels": 0
                            },
                            {
                                "url": "https://drive.google.com/uc?id=1uNrZTtxPwyGV8eAXRFpaqW99kZunkDvS",
                                "size": "large",
                                "widthPixels": 0,
                                "heightPixels": 0
                            }
                        ]
                    },
                    "title": "",
                    "textContent": {
                        "primaryText": {
                            "type": "PlainText",
                            "text": ""
                        }
                    },
                    "logoUrl": "https://drive.google.com/uc?id=1uNrZTtxPwyGV8eAXRFpaqW99kZunkDvS"
                }
            }
            )
        )
        return handler_input.response_builder.response

class RecordsIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("RecordsIntent")(handler_input)
    def handle(self, handler_input):
        global answerSlotKey
        global level
        global score
        global triviaQuestions
        global triviaScore
        global question
        global randOption
        # type: (HandlerInput) -> Response

        speech_text = "Tu puntaje actual es de " + str(score) + " y estás en el nivel " + str(level) + " de 6 disponibles"
        handler_input.response_builder.speak(speech_text).set_should_end_session(
            False).add_directive(
            RenderDocumentDirective(
                document=_load_apl_document("records.json"),
                datasources={
                "bodyTemplate1Data": {
                    "type": "object",
                    "objectId": "bt1Sample",
                    "backgroundImage": {
                        "sources": [
                            {
                                "url": "https://drive.google.com/uc?id=1jvdf4X_eOubzE9boK7BC2d_4UR-_Uv4s",
                                "size": "small",
                                "widthPixels": 0,
                                "heightPixels": 0
                            },
                            {
                                "url": "https://drive.google.com/uc?id=1jvdf4X_eOubzE9boK7BC2d_4UR-_Uv4s",
                                "size": "large",
                                "widthPixels": 0,
                                "heightPixels": 0
                            }
                        ]
                    },
                    "title": "",
                    "textContent": {
                        "primaryText": {
                            "type": "PlainText",
                            "text": ""
                        }
                    },
                    "logoUrl": "https://drive.google.com/open?id=1-Zs5Z4CXpLp1f2yywK94PmbW_gvvmgtE"
                }
            }
            )
        )
        return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    global randOption
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response


        speech_text = dataMap['ayuda_{}'.format(randOption(3))]

        handler_input.response_builder.speak(speech_text).ask(
            speech_text).add_directive(
            RenderDocumentDirective(
                document=_load_apl_document("help.json"),
                datasources={
                "bodyTemplate1Data": {
                    "type": "object",
                    "objectId": "bt1Sample",
                    "backgroundImage": {
                        "sources": [
                            {
                                "url": "https://drive.google.com/uc?id=1sSjQUM6FC_rsloCTx5qXEAdWDjkz18W9",
                                "size": "small",
                                "widthPixels": 0,
                                "heightPixels": 0
                            },
                            {
                                "url": "https://drive.google.com/uc?id=1sSjQUM6FC_rsloCTx5qXEAdWDjkz18W9",
                                "size": "large",
                                "widthPixels": 0,
                                "heightPixels": 0
                            }
                        ]
                    },
                    "title": "",
                    "textContent": {
                        "primaryText": {
                            "type": "PlainText",
                            "text": ""
                        }
                    },
                    "logoUrl": "https://drive.google.com/uc?id=1uNrZTtxPwyGV8eAXRFpaqW99kZunkDvS"
                }
            }
            )
            )
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = dataMap['goodbye']

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = (
            "Vamos a entrenar "
            "Intenta de nuevo")
        reprompt = "You can say hello!!"
        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speech = "He tenido un pequeño tropiezo. Intenta de nuevo, por favor"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response

##General functions of the skills

def randOption(numOptions):
    return randint(0, numOptions-1)

def rand4ElementsList():
    list = [randint(1,8),randint(1,8),randint(1,8),randint(1,8)]
    return list

def _load_apl_document(file_path):
    # type: (str) -> Dict[str, Any]
    """Load the apl json document at the path into a dict object."""
    with open(file_path) as f:
        return json.load(f)

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(TrainingIntentHandler())
sb.add_request_handler(TriviaIntentHandler())
sb.add_request_handler(RecordsIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()
