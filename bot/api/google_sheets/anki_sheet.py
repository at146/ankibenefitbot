import json
from zoneinfo import ZoneInfo

import gspread

from bot.core.config import settings
from bot.crud import answers_questions_db, users_channel_db, users_db, users_lidmagnit_db
from bot.db.session import db_session
from bot.dialogs.menu.questioning.text import DICT_QUESTIONS, LAST_QUESTION
from bot.init import log


class AnkiSheet:
    def __init__(self, path_credits: str) -> None:
        self.path_credits = path_credits
        self.gs = gspread.auth.service_account(self.path_credits)
        # подключаем таблицу по ID
        self.table = self.gs.open_by_key(settings.GOOGLE_SHEET_TABLE_ID)

        self.header_worksheet_1 = self._get_header_worksheet_1()
        self.header_a1_worksheet_1 = f"A1:{gspread.utils.rowcol_to_a1(1, len(self.header_worksheet_1))}"

        self.header_worksheet_2 = ["Ник ТГ", "Дата и Время входа", "Забрал статью", "Перешел в канал"]
        self.header_a1_worksheet_2 = f"A1:{gspread.utils.rowcol_to_a1(1, len(self.header_worksheet_2))}"

        self.header_worksheet_3 = ["Ник ТГ", "Дата и Время входа"]
        self.header_a1_worksheet_3 = f"A1:{gspread.utils.rowcol_to_a1(1, len(self.header_worksheet_3))}"

        self.header_worksheet_4 = ["Ник ТГ", "Дата и Время входа", "Забрал статью", "Перешел в канал"]
        self.header_a1_worksheet_4 = f"A1:{gspread.utils.rowcol_to_a1(1, len(self.header_worksheet_4))}"

    async def init_table(self) -> None:
        try:
            self.worksheet_1 = self.table.worksheet("Лист1")
        except gspread.exceptions.WorksheetNotFound:
            self.worksheet_1 = self.table.add_worksheet("Лист1", rows=0, cols=0, index=0)
        try:
            self.worksheet_2 = self.table.worksheet("Лист2")
        except gspread.exceptions.WorksheetNotFound:
            self.worksheet_2 = self.table.add_worksheet("Лист2", rows=0, cols=0, index=1)
        try:
            self.worksheet_3 = self.table.worksheet("Лист3")
        except gspread.exceptions.WorksheetNotFound:
            self.worksheet_3 = self.table.add_worksheet("Лист3", rows=0, cols=0, index=2)
        try:
            self.worksheet_4 = self.table.worksheet("лидмагнит")
        except gspread.exceptions.WorksheetNotFound:
            self.worksheet_4 = self.table.add_worksheet("лидмагнит", rows=0, cols=0, index=3)
        await self._init_worksheet_1()
        await self._init_worksheet_2()
        await self._init_worksheet_3()
        await self._init_worksheet_4()

    def _get_header_worksheet_1(self) -> list[str]:
        header_list = ["Ник ТГ", "Дата и Время входа"]
        for value in DICT_QUESTIONS.values():
            header_list.append(value["question"])  # type: ignore
        header_list.append(LAST_QUESTION["question"])  # type: ignore
        return header_list

    async def _init_worksheet_1(self) -> None:
        answers_users = await answers_questions_db.get_results(db_session)

        result_value = []
        for answers_user in answers_users:
            json_acceptable_string = answers_user.results.replace("'", '"')
            dict_value: dict[str, str] = json.loads(json_acceptable_string)
            list_question = list(dict_value.values())
            result_value.append(
                [
                    f"@{answers_user.user.username}" if answers_user.user.username else answers_user.user.first_name,
                    answers_user.user.create_datetime.astimezone(tz=ZoneInfo("Europe/Moscow")).strftime(
                        "%d/%m/%Y, %H:%M:%S"
                    ),
                    *list_question,
                ]
            )

        value_a1 = f"A2:{gspread.utils.rowcol_to_a1(len(result_value) + 1, len(self.header_worksheet_1))}"
        self.worksheet_1.batch_update(
            [
                {
                    "range": self.header_a1_worksheet_1,
                    "values": [self.header_worksheet_1],
                },
                {
                    "range": value_a1,
                    "values": result_value,
                },
            ]
        )

        formats: list[gspread.worksheet.CellFormat] = [
            {
                "range": self.header_a1_worksheet_1,
                "format": {
                    "textFormat": {
                        "bold": True,
                    },
                },
            },
            {
                "range": f"A1:{gspread.utils.rowcol_to_a1(len(result_value) + 1, len(self.header_worksheet_1))}",
                "format": {
                    "wrapStrategy": "WRAP",
                    "verticalAlignment": "TOP",
                },
            },
        ]
        self.worksheet_1.batch_format(formats)

    async def _init_worksheet_2(self) -> None:
        users = await users_db.get_users(db_session)

        result_value = []
        for user in users:
            result_value.append(
                [
                    f"@{user.username}" if user.username else user.first_name,
                    user.create_datetime.astimezone(tz=ZoneInfo("Europe/Moscow")).strftime("%d/%m/%Y, %H:%M:%S"),
                    "Да" if user.is_clicked_article else "Нет",
                    "Да" if user.is_clicked_channel else "Нет",
                ]
            )

        value_a1 = f"A2:{gspread.utils.rowcol_to_a1(len(result_value) + 1, len(self.header_worksheet_2))}"
        self.worksheet_2.batch_update(
            [
                {
                    "range": self.header_a1_worksheet_2,
                    "values": [self.header_worksheet_2],
                },
                {
                    "range": value_a1,
                    "values": result_value,
                },
            ]
        )

        formats: list[gspread.worksheet.CellFormat] = [
            {
                "range": self.header_a1_worksheet_2,
                "format": {
                    "textFormat": {
                        "bold": True,
                    },
                },
            },
            {
                "range": f"A1:{gspread.utils.rowcol_to_a1(len(result_value) + 1, len(self.header_worksheet_2))}",
                "format": {
                    "wrapStrategy": "WRAP",
                    "verticalAlignment": "TOP",
                },
            },
        ]
        self.worksheet_2.batch_format(formats)

    async def _init_worksheet_3(self) -> None:
        users_channel = await users_channel_db.get_users_channel(db_session)

        result_value = []
        for user_channel in users_channel:
            result_value.append(
                [
                    f"@{user_channel.username}" if user_channel.username else user_channel.first_name,
                    user_channel.create_datetime.astimezone(tz=ZoneInfo("Europe/Moscow")).strftime(
                        "%d/%m/%Y, %H:%M:%S"
                    ),
                ]
            )

        value_a1 = f"A2:{gspread.utils.rowcol_to_a1(len(result_value) + 1, len(self.header_worksheet_3))}"
        self.worksheet_3.batch_update(
            [
                {
                    "range": self.header_a1_worksheet_3,
                    "values": [self.header_worksheet_3],
                },
                {
                    "range": value_a1,
                    "values": result_value,
                },
            ]
        )
        formats: list[gspread.worksheet.CellFormat] = [
            {
                "range": self.header_a1_worksheet_3,
                "format": {
                    "textFormat": {
                        "bold": True,
                    },
                },
            },
            {
                "range": f"A1:{gspread.utils.rowcol_to_a1(len(result_value) + 1, len(self.header_worksheet_3))}",
                "format": {
                    "wrapStrategy": "WRAP",
                    "verticalAlignment": "TOP",
                },
            },
        ]
        self.worksheet_3.batch_format(formats)

    async def _get_users_lidmagnit(self) -> list[list[str]]:
        users_lidmagnit = await users_lidmagnit_db.get_users_lidmagnit(db_session)
        result_value = []
        for user in users_lidmagnit:
            result_value.append(
                [
                    f"@{user.username}" if user.username else user.first_name,
                    user.create_datetime.astimezone(tz=ZoneInfo("Europe/Moscow")).strftime("%d/%m/%Y, %H:%M:%S"),
                    "Да" if user.is_clicked_article else "Нет",
                    "Да" if user.is_clicked_channel else "Нет",
                ]
            )
        return result_value

    async def _init_worksheet_4(self) -> None:
        result_value = await self._get_users_lidmagnit()
        value_a1 = f"A2:{gspread.utils.rowcol_to_a1(len(result_value) + 1, len(self.header_worksheet_4))}"
        self.worksheet_4.batch_update(
            [
                {
                    "range": self.header_a1_worksheet_4,
                    "values": [self.header_worksheet_4],
                },
                {
                    "range": value_a1,
                    "values": result_value,
                },
            ]
        )

        formats: list[gspread.worksheet.CellFormat] = [
            {
                "range": self.header_a1_worksheet_4,
                "format": {
                    "textFormat": {
                        "bold": True,
                    },
                },
            },
            {
                "range": f"A1:{gspread.utils.rowcol_to_a1(len(result_value) + 1, len(self.header_worksheet_4))}",
                "format": {
                    "wrapStrategy": "WRAP",
                    "verticalAlignment": "TOP",
                },
            },
        ]
        self.worksheet_4.batch_format(formats)

    async def update_table(self) -> None:
        try:
            await self._update_worksheet_1()
            await self._update_worksheet_2()
            await self._update_worksheet_3()
            await self._update_worksheet_4()
        except Exception as ex:
            log.exception(ex)

    async def _update_worksheet_1(self) -> None:
        answers_users = await answers_questions_db.get_results(db_session)

        result_value = []
        for answers_user in answers_users:
            json_acceptable_string = answers_user.results.replace("'", '"')
            dict_value: dict[str, str] = json.loads(json_acceptable_string)
            list_question = list(dict_value.values())
            result_value.append(
                [
                    f"@{answers_user.user.username}" if answers_user.user.username else answers_user.user.first_name,
                    answers_user.user.create_datetime.astimezone(tz=ZoneInfo("Europe/Moscow")).strftime(
                        "%d/%m/%Y, %H:%M:%S"
                    ),
                    *list_question,
                ]
            )

        if result_value:
            gs = gspread.auth.service_account(self.path_credits)
            table = gs.open_by_key(settings.GOOGLE_SHEET_TABLE_ID)
            worksheet_1 = table.worksheet("Лист1")
            value_a1 = f"A2:{gspread.utils.rowcol_to_a1(len(result_value) + 1, len(self.header_worksheet_1))}"
            worksheet_1.batch_update(
                [
                    {
                        "range": self.header_a1_worksheet_1,
                        "values": [self.header_worksheet_1],
                    },
                    {
                        "range": value_a1,
                        "values": result_value,
                    },
                ]
            )
            formats: list[gspread.worksheet.CellFormat] = [
                {
                    "range": self.header_a1_worksheet_1,
                    "format": {
                        "textFormat": {
                            "bold": True,
                        },
                    },
                },
                {
                    "range": f"A1:{gspread.utils.rowcol_to_a1(len(result_value) + 1, len(self.header_worksheet_1))}",
                    "format": {
                        "wrapStrategy": "WRAP",
                        "verticalAlignment": "TOP",
                    },
                },
            ]
            worksheet_1.batch_format(formats)

    async def _update_worksheet_2(self) -> None:
        users = await users_db.get_users(db_session)

        result_value = []
        for user in users:
            result_value.append(
                [
                    f"@{user.username}" if user.username else user.first_name,
                    user.create_datetime.astimezone(tz=ZoneInfo("Europe/Moscow")).strftime("%d/%m/%Y, %H:%M:%S"),
                    "Да" if user.is_clicked_article else "Нет",
                    "Да" if user.is_clicked_channel else "Нет",
                ]
            )

        if result_value:
            gs = gspread.auth.service_account(self.path_credits)
            table = gs.open_by_key(settings.GOOGLE_SHEET_TABLE_ID)
            worksheet_2 = table.worksheet("Лист2")
            value_a1 = f"A2:{gspread.utils.rowcol_to_a1(len(result_value) + 1, len(self.header_worksheet_2))}"
            worksheet_2.batch_update(
                [
                    {
                        "range": self.header_a1_worksheet_2,
                        "values": [self.header_worksheet_2],
                    },
                    {
                        "range": value_a1,
                        "values": result_value,
                    },
                ]
            )

            formats: list[gspread.worksheet.CellFormat] = [
                {
                    "range": self.header_a1_worksheet_2,
                    "format": {
                        "textFormat": {
                            "bold": True,
                        },
                    },
                },
                {
                    "range": f"A1:{gspread.utils.rowcol_to_a1(len(result_value) + 1, len(self.header_worksheet_2))}",
                    "format": {
                        "wrapStrategy": "WRAP",
                        "verticalAlignment": "TOP",
                    },
                },
            ]
            worksheet_2.batch_format(formats)

    async def _update_worksheet_3(self) -> None:
        users_channel = await users_channel_db.get_users_channel(db_session)

        result_value = []
        for user_channel in users_channel:
            result_value.append(
                [
                    f"@{user_channel.username}" if user_channel.username else user_channel.first_name,
                    user_channel.create_datetime.astimezone(tz=ZoneInfo("Europe/Moscow")).strftime(
                        "%d/%m/%Y, %H:%M:%S"
                    ),
                ]
            )

        if result_value:
            gs = gspread.auth.service_account(self.path_credits)
            table = gs.open_by_key(settings.GOOGLE_SHEET_TABLE_ID)
            worksheet_3 = table.worksheet("Лист3")
            value_a1 = f"A2:{gspread.utils.rowcol_to_a1(len(result_value) + 1, len(self.header_worksheet_3))}"
            worksheet_3.batch_update(
                [
                    {
                        "range": self.header_a1_worksheet_3,
                        "values": [self.header_worksheet_3],
                    },
                    {
                        "range": value_a1,
                        "values": result_value,
                    },
                ]
            )
            formats: list[gspread.worksheet.CellFormat] = [
                {
                    "range": self.header_a1_worksheet_3,
                    "format": {
                        "textFormat": {
                            "bold": True,
                        },
                    },
                },
                {
                    "range": f"A1:{gspread.utils.rowcol_to_a1(len(result_value) + 1, len(self.header_worksheet_3))}",
                    "format": {
                        "wrapStrategy": "WRAP",
                        "verticalAlignment": "TOP",
                    },
                },
            ]
            worksheet_3.batch_format(formats)

    async def _update_worksheet_4(self) -> None:
        result_value = await self._get_users_lidmagnit()

        if result_value:
            gs = gspread.auth.service_account(self.path_credits)
            table = gs.open_by_key(settings.GOOGLE_SHEET_TABLE_ID)
            worksheet_4 = table.worksheet("лидмагнит")
            value_a1 = f"A2:{gspread.utils.rowcol_to_a1(len(result_value) + 1, len(self.header_worksheet_4))}"
            worksheet_4.batch_update(
                [
                    {
                        "range": self.header_a1_worksheet_4,
                        "values": [self.header_worksheet_4],
                    },
                    {
                        "range": value_a1,
                        "values": result_value,
                    },
                ]
            )

            formats: list[gspread.worksheet.CellFormat] = [
                {
                    "range": self.header_a1_worksheet_4,
                    "format": {
                        "textFormat": {
                            "bold": True,
                        },
                    },
                },
                {
                    "range": f"A1:{gspread.utils.rowcol_to_a1(len(result_value) + 1, len(self.header_worksheet_4))}",
                    "format": {
                        "wrapStrategy": "WRAP",
                        "verticalAlignment": "TOP",
                    },
                },
            ]
            worksheet_4.batch_format(formats)
