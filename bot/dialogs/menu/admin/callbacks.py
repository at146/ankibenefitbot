import asyncio
from datetime import datetime
from logging import Logger

from aiogram import Bot
from aiogram.exceptions import (
    TelegramAPIError,
    TelegramBadRequest,
    TelegramForbiddenError,
    TelegramNotFound,
    TelegramRetryAfter,
)
from aiogram.types import InlineKeyboardMarkup, Message, User
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.crud import users_db, users_lidmagnit_db


async def admin_text_spam(
    message: Message,
    message_input: MessageInput,
    manager: DialogManager,
) -> None:
    await message.delete()

    db_session: async_sessionmaker[AsyncSession] = manager.middleware_data["db_session"]
    log: Logger = manager.middleware_data["log"]
    bot: Bot = manager.middleware_data["bot"]
    event_from_user: User = manager.middleware_data["event_from_user"]

    count_users_in_bot = 0
    count_users_got_msg = 0

    users_lidmagnit = await users_lidmagnit_db.get_users_lidmagnit(db_session)
    users = await users_db.get_users(db_session)
    users_ids = [user.user_id for user in users_lidmagnit] + [user.user_id for user in users]
    unique_users_ids = set(users_ids)
    len_users = len(unique_users_ids)

    new_text = f"Дождитесь завершения рассылки!\n\nОтправка [0 из {len_users}]"
    last_message = await message.answer(text=new_text)

    log.info("[%s] %s: нажал рассылку", event_from_user.id, event_from_user.full_name)

    disable_web_page_preview: bool = manager.find("disable_web_page_preview").is_checked()  # type: ignore

    if message.photo and message.photo[-1].file_id:
        photo = message.photo[-1].file_id
    else:
        photo = None

    if message.video and message.video.file_id:
        video = message.video.file_id
    else:
        video = None

    if message.animation and message.animation.file_id:
        animation = message.animation.file_id
    else:
        animation = None

    start_spam = datetime.now()

    try:
        for user_id in unique_users_ids:
            if user_id == event_from_user.id:
                continue
            # Всего пользователей
            count_users_in_bot += 1
            if count_users_in_bot % 1000 == 0:
                try:
                    await last_message.edit_text(
                        text=f"Дождитесь завершения рассылки!\n\nОтправка [{count_users_in_bot} из {len_users}]",
                    )
                except Exception as ex:
                    log.exception(ex)
                await asyncio.sleep(0.035)

            if await send_message_spam(
                bot=bot,
                user_id=user_id,
                text=message.html_text,
                photo=photo,
                video=video,
                animation=animation,
                reply_markup=None,
                disable_web_page_preview=disable_web_page_preview,
                log=log,
            ):
                # Кому отправилось
                count_users_got_msg += 1
            await asyncio.sleep(0.035)
    except Exception as ex:
        log.exception(ex)

    finish_spam = datetime.now() - start_spam

    log.info("[%s] %s: завершил рассылку", event_from_user.id, event_from_user.full_name)

    await last_message.delete()

    new_text = (
        f"Рассылка завершена!\n\n"
        f"<b>Пользователей (всего/активных): {count_users_in_bot}/{count_users_got_msg}</b>.\n\n"
        f"Время завершения: {datetime.now().strftime('%H:%M %d.%m.%Y')}\n"
        f"Длительность: {finish_spam}"
    )

    manager.dialog_data["result_spam_text"] = new_text

    await manager.next()


async def send_message_spam(  # noqa: C901
    bot: Bot,
    user_id: int,
    text: str,
    photo: str | None,
    video: str | None,
    animation: str | None,
    reply_markup: InlineKeyboardMarkup | None,
    disable_web_page_preview: bool,
    log: Logger,
) -> bool:
    try:
        if photo:
            await bot.send_photo(user_id, photo=photo, caption=text, reply_markup=reply_markup)
        elif video:
            await bot.send_video(user_id, video=video, caption=text, reply_markup=reply_markup)
        elif animation:
            await bot.send_animation(user_id, animation=animation, caption=text, reply_markup=reply_markup)
        else:
            await bot.send_message(
                user_id, text, reply_markup=reply_markup, disable_web_page_preview=disable_web_page_preview
            )
    except TelegramBadRequest as ex:
        log.exception(ex)
    except TelegramForbiddenError:
        log.info("Target [ID:%s]: blocked by user", user_id)
    except TelegramNotFound:
        log.error("Target [ID:%s]: chat, message, user, etc. not found.", user_id)
    except TelegramRetryAfter as ex:
        log.exception(ex)
        log.exception("Target [ID:%s]: Flood limit is exceeded. Sleep %s seconds.", user_id, ex.retry_after)
        await asyncio.sleep(ex.retry_after)
        return await send_message_spam(
            bot=bot,
            user_id=user_id,
            text=text,
            photo=photo,
            video=video,
            animation=animation,
            reply_markup=reply_markup,
            disable_web_page_preview=disable_web_page_preview,
            log=log,
        )  # Recursive call
    except TelegramAPIError as ex:
        log.exception(ex)
    except Exception as ex:
        log.exception(ex)
    else:
        log.info("Target [ID:%s]: success", user_id)
        return True
    return False
