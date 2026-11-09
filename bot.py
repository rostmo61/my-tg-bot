import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# ==================== НАСТРОЙКИ ====================
BOT_TOKEN = "9163715024:AAEdQDGVu9p5gQpTfFJaEE2ncKZLFaLZ958"  # Вставь свой токен от BotFather
# Вставь ссылку на свой личный Телеграм (например, "https://t.me/your_nickname")
YOUR_TG_LINK = ""

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class Funnel(StatesGroup):
    step1 = State()
    step2 = State()
    step3 = State()  # Новый шаг с условиями
    step4 = State()

# ==================== КЛАВИАТУРЫ ====================
def step1_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔥 Да, мне интересно, как это работает", callback_data="go_step2")]
    ])

def step2_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🤔 А я подхожу под условия?", callback_data="go_step3")]
    ])

def step3_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Да, мне 18+ и у меня есть самозанятость/ИП", callback_data="go_step4")],
        [InlineKeyboardButton(text="❌ У меня нет самозанятости", url=YOUR_TG_LINK)] # Ведем сразу в ЛС
    ])

def step4_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🤔 Понятно, а в чем подвох?", callback_data="go_step5")]
    ])

def step5_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Написать мне в личку", url=YOUR_TG_LINK)]
    ])

# ==================== ХЭНДЛЕРЫ (СЦЕНАРИЙ) ====================

@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    
    # ШАГ 1. Приветствие, позиционирование и оффер
    text_1 = (
        f"👋 <b>Привет, {message.from_user.first_name}!</b>\n\n"
        "Меня зовут Дмитрий, и я являюсь <b>прямым партнером ведущих банков страны</b>: "
        "Альфа-Банк, Озон Банк, Сбер, Т-Банк, ВТБ, ОТП и многих других.\n\n"
        "Я помогаю людям получать <b>денежное вознаграждение</b> за оформление дебетовых карт и счетов. "
        "С каждого оформленного продукта ты получаешь выплату на свой счет. Чем больше карт оформишь — тем больше заработаешь.\n\n"
        "🎁 <b>Бонус:</b> За каждого приведенного друга — <b>+2000 ₽</b> сверху (это уже мой личный бонус от меня).\n\n"
        "Готов узнать, как это работает и сколько ты сможешь вывести?"
    )
    await message.answer(text_1, parse_mode="HTML", reply_markup=step1_keyboard())
    await state.set_state(Funnel.step1)


@dp.callback_query(Funnel.step1, F.data == "go_step2")
async def process_step2(callback: CallbackQuery, state: FSMContext):
    # ШАГ 2. Почему банки платят
    text_2 = (
        "📊 <b>Давай уйдем по глубже. Почему банки за это платят?</b>\n\n"
        "Всё очень просто. Банки тратят огромные бюджеты на рекламу, чтобы привлекать новых клиентов. "
        "Однако им гораздо выгоднее платить партнерам (вроде меня) за реальных людей, которые приходят и оформляют карты.\n\n"
        "💡 <b>Как это работает:</b>\n"
        "Банки мне платят за то, что я привлекаю новых клиентов в их банки. "
        "А новый клиент для банка — это как раз таки <b>ТЫ</b>.\n\n"
        "Из этой выплаты я делюсь с тобой. Ты оформляешь карту или открываешь счет по моей ссылке, "
        "банк подтверждает, что ты стал их клиентом, и я сразу перевожу тебе твое <b>денежное вознаграждение</b>.\n\n"
        "💰 <b>Сколько можно получить?</b>\n"
        "От 1 000 до 35 000 ₽ (всё зависит от тебя). "
        "Чем больше банков ты охватишь, тем больше денег выведешь.\n\n"
        "🎁 И повторюсь: если ты приведешь друга, который тоже оформит карту, я лично переведу тебе <b>+2000 ₽ сверху</b>.\n\n"
        "Но прежде чем мы продолжим, давай проверим, подходишь ли ты под требования банков."
    )
    await callback.message.edit_text(text_2, parse_mode="HTML")
    await callback.message.answer("👇", reply_markup=step2_keyboard())
    await state.set_state(Funnel.step2)
    await callback.answer()


@dp.callback_query(Funnel.step2, F.data == "go_step3")
async def process_step3(callback: CallbackQuery, state: FSMContext):
    # ШАГ 3. Требования (Квалификация лида)
    text_3 = (
        "📋 <b>Важное условие для получения вознаграждения:</b>\n\n"
        "Банки имеют строгие правила. Чтобы получить выплату за оформление карты или счета, ты должен соответствовать двум критериям:\n\n"
        "1️⃣ <b>Тебе должно быть 18 лет или больше.</b>\n\n"
        "2️⃣ <b>У тебя должна быть самозанятость или ИП/ООО.</b> "
        "(Банки платят партнерам повышенные бонусы именно за бизнес-клиентов и самозанятых).\n\n"
        "⚠️ <b>Если у тебя нет самозанятости или ИП</b> — не расстраивайся. Нажми на кнопку ниже, переходи ко мне в личку, и я помогу тебе её оформить (это бесплатно и займет 5 минут).\n\n"
        "Ну что, подходишь под условия?"
    )
    await callback.message.edit_text(text_3, parse_mode="HTML")
    await callback.message.answer("Выбери вариант ниже 👇", reply_markup=step3_keyboard())
    await state.set_state(Funnel.step3)
    await callback.answer()


@dp.callback_query(Funnel.step3, F.data == "go_step4")
async def process_step4(callback: CallbackQuery, state: FSMContext):
    # ШАГ 4. Снятие сомнений (для тех, кто подошел)
    text_4 = (
        "🛡 <b>Отлично! Тогда снимаю все оставшиеся сомнения:</b>\n\n"
        "1️⃣ <b>Это официально.</b> Ты оформляешь карту напрямую на официальном сайте банка (через мою ссылку). Никаких серых схем и левых приложений.\n\n"
        "2️⃣ <b>Тебе не нужно платить.</b> Обслуживание карт чаще всего бесплатное. Ты не тратишь ни копейки, а только получаешь вознаграждение.\n\n"
        "3️⃣ <b>Абсолютная безопасность.</b> Твои данные вводятся на защищенных серверах банков. Я не вижу твои паспортные данные или номера счетов.\n\n"
        "4️⃣ <b>Выплаты честные.</b> Как только банк подтверждает, что ты стал клиентом, я сразу перевожу тебе деньги. Без задержек.\n\n"
        "Всё прозрачно и выгодно для тебя. Остались вопросы?"
    )
    await callback.message.edit_text(text_4, parse_mode="HTML")
    await callback.message.answer("👇", reply_markup=step4_keyboard())
    await state.set_state(Funnel.step4)
    await callback.answer()


@dp.callback_query(Funnel.step4, F.data == "go_step5")
async def process_step5(callback: CallbackQuery, state: FSMContext):
    # ШАГ 5. Перевод в личку (для тех, кто подошел)
    text_5 = (
        "🤝 <b>Супер! Ты подходишь под все условия.</b>\n\n"
        "В боте я не могу дать тебе персональные ссылки на банки и показать актуальные размеры выплат на сегодняшний день. "
        "Поэтому предлагаю перейти в мой личный Телеграм.\n\n"
        "Там я скину тебе:\n"
        "✅ Ссылки на карты с максимальными выплатами прямо сейчас\n"
        "✅ Условия по моему бонусу +2000 ₽ за друга\n"
        "✅ Отвечу на любые вопросы\n\n"
        "<b>Жми на кнопку ниже и пиши мне «ПРИВЕТ». Я уже жду!</b> 👇"
    )
    await callback.message.edit_text(text_5, parse_mode="HTML")
    await callback.message.answer("🚀", reply_markup=step5_keyboard())
    await state.clear()
    await callback.answer()


# ==================== ЗАПУСК ====================
async def main():
    logging.info("Бот-прогрев запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())