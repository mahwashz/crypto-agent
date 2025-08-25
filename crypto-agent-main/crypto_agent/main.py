# 📁 main.py
import asyncio
import chainlit as cl
from agent.crypto_agent import run_agent
from alerts.alerts import check_alerts

# 🔁 Background alert checker every 30 seconds
async def background_alert_loop():
    while True:
        await asyncio.sleep(30)
        check_alerts()

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("background_task", asyncio.create_task(background_alert_loop()))
    await cl.Message(content="""
👋 Welcome to Crypto Agent! Ask me things like:
- `What is the price of BTC?`
- `Alert me when ETH > 3500`
- `Show BTC chart`

I'll notify you via 🔔 Chainlit UI + 📩 email when your alert triggers!
""").send()

@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content
    result = await run_agent(user_input)

    # If chart is returned
    if isinstance(result, tuple):
        text, chart_path = result
        await cl.Message(content=text).send()
        await cl.Message(content="", elements=[cl.Image(path=chart_path, name="chart")]).send()
    else:
        await cl.Message(content=result).send()
