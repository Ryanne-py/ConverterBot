from aiogram.dispatcher import Dispatcher
from aiogram.types import ContentType
from aiogram.utils import executor
import logging
from aiogram import Bot
from aiogram import base
import bot_token
from aiogram import types as tp
import api_service
import keyboards as kb
import many_conver

class Bot(Bot):
    def

bot = Bot(bot_token.BOT_TOKEN)
dp = Dispatcher(bot)

PRICE = tp.LabeledPrice(label="Activation for 1 month", amount=5*100)

privat_api = api_service.PrivatAPI()
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start', )
async def start(message: tp.Message):
    await message.answer('Functional menu', reply_markup=kb.keyboard_start)


@dp.callback_query_handler(text='donate')
async def help(call: tp.CallbackQuery):
    if bot_token.PAYMANT_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(call.message.chat.id, "Test payment, money will not be debited")

    await bot.send_invoice(
        call.message.chat.id,
        title="Bot subscription",
        description="Bot subscription activation for 1 month",
        provider_token=bot_token.PAYMANT_TOKEN,
        currency="usd",
        photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
        photo_width=416,
        photo_height=234,
        photo_size=416,
        is_flexible=False,
        prices=[PRICE],
        start_parameter="one-month-subscription",
        payload="test-invoice-payload"
    )


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: tp.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: tp.Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    await bot.send_message(
        message.chat.id,
        f"Payment for the amount {message.successful_payment.total_amount // 100}"
        f" {message.successful_payment.currency} passed successfully")


@dp.callback_query_handler(text='help')
async def help(call: tp.CallbackQuery):
    await call.message.answer(
        'This bot was created to serve as a tool for analytics and monitoring'
        ' of exchange rates in the state bank of the country PrivatBank and conversion\n'
        'Use the start command to call the functionality menu',
        reply_markup=kb.keyboard_start
    )


@dp.message_handler(commands='con')
async def convert(message: tp.Message):
    convert_data: str = message.text[5:].split()
    try:
        await message.answer(
            f"Result - {many_convert.conversion(*convert_data)} {convert_data[2]}",
            reply_markup=kb.keyboard_start
        )

    except many_convert.CurrencyNameError:
        await message.answer(
            'Wrong currency name, you can find out the currency code for conversion at\n'
            'https://www.iban.com/currency-codes',
            reply_markup=kb.keyboard_start
        )
    except TypeError:
        await message.answer(
            'Wrong command,use \con like this\n'
            'For example "/con USD 100 UAH"'
        )


@dp.callback_query_handler(text='banks_tariffs')
async def chose_rate(call: tp.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=kb.keyboard_money_format)


@dp.callback_query_handler(text='cash_rate')
async def chose_rate(call: tp.CallbackQuery):
    await call.message.answer(f'PrivatBank cash rate (in branches):\n{privat_api.get_cash_rate()}',
                              reply_markup=kb.keyboard_start)


@dp.callback_query_handler(text='non-cash_rate')
async def chose_rate(call: tp.CallbackQuery):
    await call.message.answer(f'Non-cash rate of PrivatBank (conversion by cards, Privat24, replenishment of deposits):\n'
                              f'{privat_api.get_сashless_rate()}', reply_markup=kb.keyboard_start)


@dp.callback_query_handler(text='back')
async def back(call: tp.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=kb.keyboard_start)


@dp.callback_query_handler(text='currency_conversion')
async def currency_conversion(call: tp.CallbackQuery):
    await call.message.answer('Currency conversion.\nUse command /con\nYou can find out the currency code'
                              ' for conversion at https://www.iban.com/currency-codes\n'
                              'For example "/con USD UAH 100"')


if __name__ == '__main__':
     executor.start_polling(dp)