import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# 🔑 CONFIGURACIÓN
# El token se carga automáticamente desde las variables de entorno de Render
TOKEN_BOT = os.getenv("TOKEN_BOT")
ID_DUENO = 6618769756
SALDOS_TRADING = {}

# Configuración de logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 🚀 COMANDO PRINCIPAL
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuario_id = update.effective_user.id
    nombre = update.effective_user.first_name
    if usuario_id not in SALDOS_TRADING:
        SALDOS_TRADING[usuario_id] = 1000.0

    texto = (
        f"🎮 ¡QUÉ LO QUÉ, {nombre.upper()}! ¡BIENVENIDO AL CLUB!\n\n"
        f"💰 Tu Saldo Demo: ${SALDOS_TRADING[usuario_id]:,.2f} VegaCoins\n\n"
        f"🔥 ¡Multiplica tus monedas en Cripto Express!"
    )
    
    botones = [
        [InlineKeyboardButton("🎮 Jugar Cripto Express", web_app=WebAppInfo(url="https://github.io"))],
        [InlineKeyboardButton("💳 RECARGAR CUENTA", callback_data="menu_bancos")],
        [InlineKeyboardButton("📈 Cripto & Trading", callback_data="menu_trading")],
        [InlineKeyboardButton("🎲 Juegos Rápidos", callback_data="menu_azar")],
        [InlineKeyboardButton("⚙️ Panel Admin", callback_data="menu_admin")]
    ]
    
    reply_markup = InlineKeyboardMarkup(botones)
    if update.message: await update.message.reply_text(texto, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query: await update.callback_query.edit_message_text(texto, reply_markup=reply_markup, parse_mode="Markdown")

# 🎛️ MANEJADOR DE BOTONES
async def procesar_botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "volver_inicio":
        await start(update, context)
    else:
        await query.edit_message_text("Menú en proceso de configuración.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("↩️ Volver", callback_data="volver_inicio")]]))

async def juego_dados(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_dice(emoji="🎲")

def main():
    if not TOKEN_BOT:
        print("ERROR: No se encontró el TOKEN_BOT en las variables de entorno.")
        return

    # Construcción correcta para versión moderna
    app = ApplicationBuilder().token(TOKEN_BOT).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dados", juego_dados))
    app.add_handler(CallbackQueryHandler(procesar_botones))
    
    print("🚀 BOT INICIADO CORRECTAMENTE...")
    app.run_polling()

if __name__ ==" __main__':
    main()
