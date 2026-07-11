import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# 🔑 CONFIGURACIÓN
TOKEN_SECRETO = "8226493019:AAGCbFYGDSzpRoh7Pk7wtKWPGaWh4v-OfRY"
ID_DUENO = 6618769756
ADMINISTRADORES = [ID_DUENO]
SALDOS_TRADING = {}

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
        f"🔥 ¡Multiplica tus monedas gratis en Cripto Express o recarga saldo real para competir por premios en efectivo!"
    )
    
    botones = [
        [InlineKeyboardButton("🎮 Jugar Cripto Express", web_app=WebAppInfo(url="https://github.io"))],
        [InlineKeyboardButton("💳 RECIBIMOS TODO: RECARGAR CUENTA", callback_data="menu_bancos")],
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
    
    if query.data == "menu_trading":
        await query.edit_message_text("📈 Simulador activo. (Usa el botón principal de arriba para jugar Cripto Express en vivo).", 
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("↩️ Volver", callback_data="volver_inicio")]]), parse_mode="Markdown")
    elif query.data == "menu_azar":
        await query.edit_message_text("🎲 Escribe /dados para tirar suerte.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("↩️ Volver", callback_data="volver_inicio")]]), parse_mode="Markdown")
    elif query.data == "menu_admin":
        await query.edit_message_text("⚙️ Modo Admin activo.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("↩️ Volver", callback_data="volver_inicio")]]), parse_mode="Markdown")
    
    # 🏦 MENÚ DE RECARGAS DE TODO TIPO (EFECTIVO Y MULTI-DIVISA)
    elif query.data == "menu_bancos":
        texto_bancos = (
            "💳 SISTEMA DE DEPOSITOS Y RECARGAS GENERALES 🇩🇴🇺🇸🇪🇺\n\n"
            "Aquí recibimos de todo para que no te quedes fuera. ¡Elige tu método preferido!:\n\n"
            "💵 Aceptamos montos desde: $50, $100, $200, $500, $1000, $2000, $3000 o más.\n"
            "💱 Monedas: Pesos Dominicanos (RD$), Dólares (US$), Euros (€) y Efectivo.\n\n"
            "Selecciona dónde deseas depositar tu dinero para activar tus créditos:"
        )
        botones_bancos = [
            [InlineKeyboardButton("🏦 Banreservas (RD$ / US$)", callback_data="info_reservas")],
            [InlineKeyboardButton("🏦 Banco Popular (RD$ / US$)", callback_data="info_popular")],
            [InlineKeyboardButton("🏦 Banco BHD (RD$ / €)", callback_data="info_bhd")],
            [InlineKeyboardButton("🤝 Depósito en Efectivo / Caribe Express", callback_data="info_efectivo")],
            [InlineKeyboardButton("↩️ Volver al Inicio", callback_data="volver_inicio")]
        ]
        await query.edit_message_text(texto_bancos, reply_markup=InlineKeyboardMarkup(botones_bancos), parse_mode="Markdown")
        
    elif query.data in ["info_reservas", "info_popular", "info_bhd", "info_efectivo"]:
        if query.data == "info_efectivo":
            texto_instrucciones = (
                "🤝 RECARGAS EN EFECTIVO / REMESAS\n\n"
                "Si tienes efectivo o deseas enviar por remesa (Caribe Express, Western Union, etc.):\n\n"
                "1️⃣ Escríbele directamente al administrador del bot indicando la cantidad que deseas recargar (Aceptamos 50, 100, 500, 1000, 2000, 3000 pesos, dólares o euros).\n"
                "2️⃣ Coordina la entrega del efectivo o envía el código de remesa correspondiente.\n\n"
                "⚡ ¡Tu saldo se activará inmediatamente al validar el dinero!"
            )
        else:
            banco_sel = ""
            if query.data == "info_reservas": banco_sel = "BANRESERVAS"
            elif query.data == "info_popular": banco_sel = "BANCO POPULAR"
            elif query.data == "info_bhd": banco_sel = "BANCO BHD"
            
            texto_instrucciones = (
                f"📥 TRANSFERENCIA BANCARIA - {banco_sel}\n\n"
                f"Realiza tu transferencia en pesos RD$, dólares americanos US$ o euros €:\n\n"
                f"📌 Banco: {banco_sel}\n"
                f"📌 Tipo: Cuenta de Ahorros / Corriente\n"
                f"📌 Número: 000-000000-0 (Pon tu número real aquí)\n"
                f"📌 Titular: Tu Nombre Comercial\n\n"
                f"💵 Monto: Recibimos transferencias de 100, 500, 2000, 3000 en adelante.\n\n"
                f"⚠️ Paso obligatorio: Una vez hecha la transferencia, envía el capture de tu comprobante a este chat para acreditar tus fondos."
            )
            
        await query.edit_message_text(texto_instrucciones, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("↩️ Volver a Opciones", callback_data="menu_bancos")]]), parse_mode="Markdown")
        
    elif query.data == "volver_inicio":
        await start(update, context)

async def juego_dados(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_dice(emoji="🎲")

def main():
    app = Application.builder().token(TOKEN_SECRETO).read_timeout(30.0).write_timeout(30.0).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dados", juego_dados))
    app.add_handler(CallbackQueryHandler(procesar_botones))
    print("🚀 BOT CONFIGURADO CON MULTI-DIVISAS Y EFECTIVO...")
    app.run_polling()

if __name__ == '__main__':
    main()
