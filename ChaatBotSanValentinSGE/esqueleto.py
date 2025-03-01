from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

import logging
import pandas as pd

TOKEN = "8094790083:AAG3avVXNxsjeLWbklMYy2fJoDwgKRB1qrQ"

#---------------------------LOGGER CONFIRM-------------------------------------

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# ------------------------------- usuarios parejas -------------------------------

datosUsuarios = {
    'usuario' : ['Alejandro Gómez', 'Carlos Pérez', 'Luis Fernández', 'Miguel Ramírez', 'David Torres',
                'Andrés Herrera', 'Javier Castro', 'Francisco Vargas', 'Manuel Rojas', 'Pablo Díaz',
                'Raúl Silva', 'Héctor Domínguez', 'Tomás Fuentes', 'Emilio Carrasco', 'Sergio Núñez',
                'Gabriel Paredes', 'Ricardo Salazar', 'Jorge Guzmán', 'Fernando León', 'Esteban Cordero',
                'Marta López', 'Ana Martínez', 'Elena Sánchez', 'Carmen Jiménez', 'Laura Molina',
                'Isabel Ortega', 'Beatriz Navarro', 'Sofía Aguilar', 'Clara Mendoza', 'Julia Vega',
                'Lucía Herrera', 'Patricia Ríos', 'Gabriela Morales', 'Verónica Peña', 'Adriana Solís',
                'Natalia Ferrer', 'Daniela Rubio', 'Carolina Espinoza', 'Valeria Montoya', 'Mariana Castro', 'Maria Fernadez'],

    'genero_deseado' : ['Hombre', 'Hombre', 'Hombre', 'Hombre', 'Hombre', 'Hombre', 'Hombre', 'Hombre', 'Hombre','Hombre',
                        'Hombre', 'Hombre', 'Hombre', 'Hombre', 'Hombre', 'Hombre', 'Hombre', 'Hombre', 'Hombre','Hombre',
                        'Mujer', 'Mujer', 'Mujer', 'Mujer', 'Mujer', 'Mujer', 'Mujer', 'Mujer', 'Mujer', 'Mujer',
                        'Mujer', 'Mujer', 'Mujer', 'Mujer', 'Mujer', 'Mujer', 'Mujer', 'Mujer', 'Mujer', 'Mujer', 'Mujer'],

    'edad' : [20, 22, 30, 40, 21, 18, 25, 38, 28, 41, 25, 34, 24, 18, 23, 25, 28, 32, 27, 29,
            35, 45, 50, 26, 31, 42, 37, 55, 48, 22, 39, 44, 33, 51, 46, 19, 53, 36, 47, 28, 26],

    'prioridad' : ['Estudio', 'Fiesta', 'Viajes', 'Deporte', 'Fiesta', 'Estudio', 'Deporte', 'Viajes', 'Estudio','Fiesta',
                   'Viajes', 'Deporte', 'Estudio', 'Fiesta', 'Deporte', 'Viajes', 'Fiesta', 'Estudio','Viajes', 'Deporte',
                    'Estudio', 'Fiesta', 'Viajes', 'Deporte', 'Fiesta','Viajes', 'Deporte', 'Estudio', 'Fiesta', 'Deporte',
                    'Viajes', 'Fiesta', 'Estudio','Viajes', 'Deporte','Fiesta', 'Estudio', 'Deporte', 'Viajes', 'Estudio', 'Fiesta'],

    'musica' : ['Rock', 'Rock', 'Reggaeton', 'Clásica', 'Rock', 'Pop', 'Reggaeton', 'Clásica', 'Rock','Reggaeton',
                'Reggaeton', 'Clásica', 'Rock', 'Pop', 'Reggaeton','Pop', 'Clásica', 'Rock', 'Reggaeton', 'Pop',
                'Reggaeton', 'Clásica', 'Rock', 'Pop', 'Reggaeton', 'Clásica', 'Rock','Reggaeton','Reggaeton', 'Clásica',
                'Pop', 'Clásica', 'Rock', 'Reggaeton', 'Pop', 'Clásica', 'Rock', 'Pop','Reggaeton', 'Clásica', 'Reggaeton'],

    'hijos': ['Sí', 'No', 'aún no lo sé', 'Sí', 'No', 'Sí', 'aún no lo sé', 'No', 'Sí','aún no lo sé',
              'No', 'Sí', 'Sí', 'No', 'aún no lo sé', 'Sí', 'No', 'Sí', 'aún no lo sé', 'No',
              'Sí', 'No', 'aún no lo sé', 'Sí', 'No', 'Sí', 'aún no lo sé', 'No','aún no lo sé', 'No',
              'aún no lo sé', 'No', 'aún no lo sé', 'No', 'aún no lo sé', 'No', 'aún no lo sé', 'No', 'aún no lo sé', 'No', 'aún no lo sé'],

    'objetivo': ['Noviazgo', 'Folleteo', 'Matrimonio', 'ya veremos que pasa', 'Folleteo', 'Noviazgo', 'Matrimonio','ya veremos que pasa',
                'Noviazgo', 'Folleteo', 'ya veremos que pasa', 'Matrimonio', 'Folleteo','Noviazgo', 'ya veremos que pasa', 'Matrimonio',
                'Noviazgo', 'Folleteo', 'Matrimonio', 'ya veremos que pasa', 'Folleteo', 'Noviazgo', 'Matrimonio','ya veremos que pasa',
                'Noviazgo', 'Matrimonio', 'ya veremos que pasa', 'Noviazgo', 'Matrimonio', 'ya veremos que pasa', 'Noviazgo', 'Matrimonio',
                'ya veremos que pasa', 'Folleteo', 'Noviazgo', 'Matrimonio', 'ya veremos que pasa', 'Matrimonio', 'ya veremos que pasa', 'Noviazgo', 'ya veremos que pasa']
}


# ------------------------------- métodos -------------------------------

async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hola {user.mention_html()}, feliz día de San Valentin!"
        "\nLos comandos disponibles son:\n"
        "/love - Iniciar el cuestionario\n"
        "/stop - Detener el cuestionario\n"
        "/back - Volver a la pregunta anterior"
       # reply_markup=ForceReply(selective=True),
    )

async def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    #logger.info(update.message.text)
    await update.message.reply_text(update.message.text)


async def cuestionario(update: Update, context: CallbackContext) -> None:
    """Send a menu."""
    keyboardOpciones = [["Mujer", "Hombre"]]
    reply_markup = ReplyKeyboardMarkup(keyboardOpciones, resize_keyboard=True, one_time_keyboard=True, selective=True)

    await update.message.reply_text("Qué estás buscando?:", reply_markup=reply_markup)


def buscar_pareja(user_data):

    parejasEncontradas = []
    puntos_totales = []

    for i in range(len(datosUsuarios['usuario'])):

        puntos = 0 #se reinicia con cada persona de la BBDD

        if datosUsuarios['genero_deseado'][i] == user_data["genero"]:
            puntos += 50

            edad_usu = datosUsuarios['edad'][i]
            edad_rango = user_data['edad']

            if edad_rango == "18-30":
                if 18 <= edad_usu <= 30:
                    puntos += 20
            elif edad_rango == "31-40":
                if 31 <= edad_usu <= 40:
                    puntos += 20
            elif edad_rango == "41-50":
                if 41 <= edad_usu <= 50:
                    puntos += 20
            elif edad_rango == "50+":
                if edad_usu >= 50:
                    puntos += 20

            if datosUsuarios['prioridad'][i] == user_data['prioridad']:
                puntos += 8
            if datosUsuarios['musica'][i] == user_data['musica']:
                puntos += 4
            if datosUsuarios['hijos'][i] ==user_data['hijos']:
                puntos += 8
            if datosUsuarios['objetivo'][i] == user_data['objetivo']:
                puntos += 10

        #Para que hagan match se necesitan 80 % y de esa forma lo agrega a la lista
        if puntos >= 80:
            parejasEncontradas.append(datosUsuarios['usuario'][i])
            puntos_totales.append(puntos)

    listaParejas = pd.DataFrame({
        'Nombre': parejasEncontradas,
        'Puntos Totales': puntos_totales
    })

    return listaParejas


async def finalizar_cuestionario(update: Update, context: CallbackContext) -> None:
    """Envía un resumen con las elecciones del usuario cuando termina el cuestionario."""

    #hace un resumen de las opciones elegidas por el usuario
    resumen = (
        f"¡Gracias por completar el cuestionario de San Valentín! Aquí está tu resumen:\n\n"
        f"**Género preferido: {context.user_data['genero']}\n"
        f"**Edad preferida: {context.user_data['edad']}\n"
        f"**Prioridad actual: {context.user_data['prioridad']}\n"
        f"**Música favorita: {context.user_data['musica']}\n"
        f"**¿Quieres tener hijos?: {context.user_data['hijos']}\n"
        f"**Qué buscas con la pareja?: {context.user_data['objetivo']}\n"
    )
    await update.message.reply_text(resumen)

    buscar_pareja(context.user_data)

    # busca la pareja dentro de los usuario de la bBDD
    df_parejas = buscar_pareja(context.user_data)

    # envia el resultdo final
    if not df_parejas.empty:

        await update.message.reply_text(f"Hemos encontrado las siguientes parejas con el % de compatibilidad :\n{df_parejas.to_string(index=False)}")
    else:
        await update.message.reply_text("No hay parejas para ti")

    # Limpiar los datos de usuario para reiniciar el cuestionario
    context.user_data.clear()


async def option_selected(update: Update, context: CallbackContext) -> None:
    """Segunda opción de árbol de decisiones"""

    text = update.message.text
    keyboardOpciones = []

    if text in ["Mujer", "Hombre"]:
        context.user_data["genero"] = text
        keyboardOpciones = [["18-30", "31-40"], ["41-50", "50+"]]
        reply_markup = ReplyKeyboardMarkup(keyboardOpciones, resize_keyboard=True, one_time_keyboard=True, selective=True)
        await update.message.reply_text("Elige tu rango de edad:", reply_markup=reply_markup)

    elif text in ["18-30", "31-40", "41-50", "50+"]:
        context.user_data["edad"] = text
        keyboardOpciones = [["Deporte", "Estudio", "Fiesta", "Viajes"], ["SALIR", "VOLVER"]]
        reply_markup = ReplyKeyboardMarkup(keyboardOpciones, resize_keyboard=True, one_time_keyboard=True, selective=True)
        await update.message.reply_text("Cuál es tu Prioridad Actual?", reply_markup=reply_markup)

    elif text in ["Deporte", "Estudio", "Fiesta", "Viajes"]:
        context.user_data["prioridad"] = text
        keyboardOpciones = [["Rock", "Reggaeton", "Clásica", "Pop"], ["SALIR", "VOLVER"]]
        reply_markup = ReplyKeyboardMarkup(keyboardOpciones, resize_keyboard=True, one_time_keyboard=True, selective=True)
        await update.message.reply_text("Cuál es tu Música favorita?", reply_markup=reply_markup)

    elif text in ["Rock", "Reggaeton", "Clásica", "Pop"]:
        context.user_data["musica"] = text
        keyboardOpciones = [["Sí", "No", "aún no lo sé"], ["SALIR", "VOLVER"]]
        reply_markup = ReplyKeyboardMarkup(keyboardOpciones, resize_keyboard=True, one_time_keyboard=True, selective=True)
        await update.message.reply_text("¿Quieres tener hijos?", reply_markup=reply_markup)

    elif text in ["Sí", "No", "aún no lo sé"]:
        context.user_data["hijos"] = text
        keyboardOpciones = [["Noviazgo", "Folleteo", "Matrimonio", "ya veremos que pasa"], ["SALIR", "VOLVER"]]
        reply_markup = ReplyKeyboardMarkup(keyboardOpciones, resize_keyboard=True, one_time_keyboard=True, selective=True)
        await update.message.reply_text("¿Para qué estás buscando pareja?", reply_markup=reply_markup)

    elif text in ["Noviazgo", "Folleteo", "Matrimonio", "ya veremos que pasa"]:
        context.user_data["objetivo"] = text

        # busca una pareja en la bbdd
        await finalizar_cuestionario(update, context)  # muestra el resumen


    elif text in ["SALIR"]:
        await update.message.reply_text("Saliendo del Chatbot de San Valentín")

    else:
        await update.message.reply_text("Opción no válida, por favor selecciona una opción correcta.")


# -------------------------------- los otros comandos -----------------------------

async def back(update: Update, context: CallbackContext) -> None:
    """volver a la pregunta anterior."""
    await update.message.reply_text("Volviendo atrás...")

async def stop(update: Update, context: CallbackContext) -> None:
    """para el cuestionario."""
    await update.message.reply_text("Se detiene el cuestionario")

# ------------------------------- main -------------------------------

def main():
    """Configura y ejecuta el bot."""
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("love", cuestionario))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("back", back))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, option_selected))

    app.run_polling()

if __name__ == "__main__":
    main()