from re import Match
from aiogram import F, Router, types
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession


from src.bot.filters.user_role_filter import UserRoleFilter
from src.bot.structure.kb.main_menu import contact, role_menu, start_menu
from src.db.requests.add_user import add_brocker, save_photographer
from src.api.dadata.api_requests import dadata_connection


class RegisterUser(StatesGroup):
    """Класс состояний для регистрации пользователя."""
    tel = State()
    full_name = State()
    role = State()
    inn = State()
    address = State()
    bik = State()
    paymant_account = State()
    broker = State()


register_user = Router()
register_user.message.filter(UserRoleFilter(user_role=None))
register_user.callback_query.filter(UserRoleFilter(user_role=None))


@register_user.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    """Обрабатывает команду /start и начинает процесс регистрации пользователя."""
    await state.clear()
    await state.update_data(telegram_id=message.from_user.id)
    await state.set_state(RegisterUser.tel)
    return await message.answer(
        "Добро пожаловать. Можно мы сохраним ваш номер?",
        reply_markup=await contact()
    )
    # await state.set_state(RegisterUser.full_name)
    # return await message.answer("Напишите свое полное ФИО", reply_markup=types.ReplyKeyboardRemove())


# @register_user.message(StateFilter(RegisterUser.full_name))
# async def get_full_name(message: types.Message, state: FSMContext):
#     last_name, name, patronymic = (
#         message.text.split(" ")
#     )
#     await state.update_data(
#         last_name=last_name,
#         name=name,
#         patronymic=patronymic
#     )


@register_user.message(StateFilter(RegisterUser.tel))
async def get_contact(
    message: types.Contact,
    state: FSMContext
):
    """Обрабатывает получение контакта и сохраняет информацию о нем."""
    if message.contact.user_id == message.from_user.id:
        await state.update_data(tel=message.contact.phone_number)
    await state.set_state(RegisterUser.inn)
    return await message.answer(
        "Пришлите ИНН",
        reply_markup=types.ReplyKeyboardRemove()
    )
    # await state.set_state(RegisterUser.role)
    # return await message.answer("Кто вы?", reply_markup=await role_menu())


# @register_user.callback_query(
#     F.data.in_(['photographer', 'broker']),
#     StateFilter(RegisterUser.role)
# )
# async def set_role(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
#     await callback.message.delete_reply_markup()
#     match callback.data:
#         case 'photographer':
#             await state.set_state(RegisterUser.inn)
#             return await callback.message.answer("Пришлите ИНН", reply_markup=types.ReplyKeyboardRemove())
#         case 'broker':
#             userdata = await state.get_data()
#             brocker = await add_brocker(session, **userdata)
#             await state.clear()
#             return await callback.message.answer(f"Мы сохранили ваши данные {brocker}", reply_markup=types.ReplyKeyboardRemove())


@register_user.message(
    StateFilter(RegisterUser.inn),
    F.text.regexp(r"\d{12}").as_("inn")
    )
async def get_inn(
    message: types.Message,
    state: FSMContext,
    inn: Match[str]
):
    """Обрабатывает получение ИНН и сохраняет информацию о нем."""
    inn = inn.group(0)
    await state.update_data(inn=int(inn))
    company, owner = dadata_connection.get_company(str(inn))
    await state.update_data(
        name=owner['name'],
        last_name=owner['last_name'],
        patronymic=owner['patronymic'],
        inn=int(inn),
        ogrnip=company['ogrn'],
        address=company['address'],
        opf_full=company['opf_full'],
        opf_short=company['opf_short'],
        )
    await state.set_state(RegisterUser.address)
    return await message.answer(
        f"{owner['name']} {owner['patronymic']}, пришлите адрес",
        reply_markup=types.ReplyKeyboardRemove()
    )


@register_user.message(
    StateFilter(RegisterUser.address),
    F.text.as_("address")
)
async def get_address(
    message: types.Message,
    state: FSMContext,
    address: Match[str]
):
    """Обрабатывает получение адреса и сохраняет информацию о нем."""
    await state.update_data(address=address)
    await state.set_state(RegisterUser.bik)
    return await message.answer(
        "Пришлите, пожалуйста, БИК",
        reply_markup=types.ReplyKeyboardRemove()
    )


@register_user.message(
    StateFilter(RegisterUser.bik),
    F.text.regexp(r"\d{9}").as_("bik")
)
async def get_bik(message: types.Message, state: FSMContext, bik: Match[str]):
    """Обрабатывает получение БИК банка и сохраняет информацию о банке."""
    try:
        bank = dadata_connection.get_bank_accaunt(str(bik.group(0)))
        await state.update_data(bank=bank)
    except ValueError:
        return await message.answer("Банк не найден. Возможно неправильно введен БИК")
    await state.set_state(RegisterUser.paymant_account)
    return await message.answer(
        "Пришлите расчетный счет",
        reply_markup=types.ReplyKeyboardRemove()
    )


@register_user.message(
    StateFilter(RegisterUser.paymant_account),
    F.text.regexp(r"\d{20}").as_("paymant_account")
)
async def get_paymant_account(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession,
    paymant_account: Match[str]
):
    """Обрабатывает получение расчетного счета и сохраняет все данные пользователя."""
    paymant_account = paymant_account.group(0)
    all_data = await state.get_data()
    all_data["paymant_account"] = paymant_account
    await save_photographer(session=session, **all_data)
    await state.clear()

    # Prepare a concise summary of the saved user data
    user_summary = (
        f"👤 Имя: {all_data['name']} {all_data['patronymic']}\n"
        f"📞 Телефон: {all_data.get('tel', 'Не указано')}\n"
        f"🆔 ИНН: {all_data['inn']}\n"
        f"🏢 Адрес: {all_data.get('address', 'Не указан')}\n"
        f"🏦 Банк: {all_data['bank']['name']}\n"
        f"💳 Расчетный счет: {all_data['paymant_account']}\n"
    )

    return await message.answer(
        f"✅ Мы успешно сохранили ваши данные:\n\n{user_summary}\n\n🎉 Регистрация завершена!",
        reply_markup=await start_menu()
    )
