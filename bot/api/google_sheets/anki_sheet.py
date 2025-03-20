import json
import uuid
from zoneinfo import ZoneInfo

import gspread

from bot.core.config import settings
from bot.crud import answers_questions_db, users_channel_db, users_db
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
        self.last_header_a1_worksheet_1 = gspread.utils.rowcol_to_a1(1, len(self.header_worksheet_1))
        self.header_worksheet_2 = self._get_header_worksheet_2()
        self.last_header_a1_worksheet_2 = gspread.utils.rowcol_to_a1(1, len(self.header_worksheet_2))
        self.header_worksheet_3 = self._get_header_worksheet_3()
        self.last_header_a1_worksheet_3 = gspread.utils.rowcol_to_a1(1, len(self.header_worksheet_3))

    async def init_table(self) -> None:
        # TODO: batch_format, format
        # вероятность очень мала))
        random_str = uuid.uuid4().hex
        self.worksheet_1 = self.table.add_worksheet(random_str, rows=0, cols=0, index=0)
        worksheets = self.table.worksheets()
        for ws in worksheets:
            if ws.index != 0:
                self.table.del_worksheet(ws)
        self.worksheet_1.update_title("Лист1")
        self.worksheet_2 = self.table.add_worksheet("Лист2", rows=0, cols=0, index=1)
        self.worksheet_3 = self.table.add_worksheet("Лист3", rows=0, cols=0, index=1)
        await self._init_worksheet_1()
        await self._init_worksheet_2()
        await self._init_worksheet_3()

    def _get_header_worksheet_1(self) -> list[str]:
        header_list = ["Ник ТГ", "Дата и Время входа"]
        for value in DICT_QUESTIONS.values():
            header_list.append(value["question"])  # type: ignore
        header_list.append(LAST_QUESTION["question"])  # type: ignore
        return header_list

    def _get_header_worksheet_2(self) -> list[str]:
        return ["Ник ТГ", "Дата и Время входа", "Забрал статью", "Перешел в канал"]

    def _get_header_worksheet_3(self) -> list[str]:
        return ["Ник ТГ", "Дата и Время входа"]

    async def _init_worksheet_1(self) -> None:
        answers_users = await answers_questions_db.get_results(db_session)
        result_cell: list[gspread.Cell] = []

        # headers
        for col, header in enumerate(self.header_worksheet_1, 1):
            cell = gspread.Cell(row=1, col=col, value=header)
            result_cell.append(cell)

        row = 2
        for answers_user in answers_users:
            json_acceptable_string = answers_user.results.replace("'", '"')
            dict_value: dict[str, str] = json.loads(json_acceptable_string)
            result_cell = result_cell + [
                gspread.Cell(
                    row,
                    col=1,
                    value=f"@{answers_user.user.username}"
                    if answers_user.user.username
                    else answers_user.user.first_name,
                ),
                gspread.Cell(
                    row,
                    col=2,
                    value=answers_user.user.create_datetime.astimezone(tz=ZoneInfo("Europe/Moscow")).strftime(
                        "%d/%m/%Y, %H:%M:%S"
                    ),
                ),
            ]
            for col, answer in enumerate(dict_value.values(), 3):
                cell = gspread.Cell(row, col=col, value=answer)
                result_cell.append(cell)
            row = row + 1

        # rect1 = gspread.utils.cell_list_to_rect(result_cell)
        self.worksheet_1.update_cells(result_cell)
        self.worksheet_1.format([f"A1:{self.last_header_a1_worksheet_1}"], {"textFormat": {"bold": True}})
        self.worksheet_1.format(
            [f"A1:{gspread.utils.rowcol_to_a1(result_cell[-1].row, result_cell[-1].col)}"],
            {"wrapStrategy": "WRAP", "verticalAlignment": "TOP"},
        )

    async def _init_worksheet_2(self) -> None:
        users = await users_db.get_users(db_session)
        result_cell: list[gspread.Cell] = []

        for col, header in enumerate(self.header_worksheet_2, 1):
            cell = gspread.Cell(row=1, col=col, value=header)
            result_cell.append(cell)

        row = 2
        for user in users:
            result_cell = result_cell + [
                gspread.Cell(row, col=1, value=f"@{user.username}" if user.username else user.first_name),
                gspread.Cell(
                    row,
                    col=2,
                    value=user.create_datetime.astimezone(tz=ZoneInfo("Europe/Moscow")).strftime("%d/%m/%Y, %H:%M:%S"),
                ),
                gspread.Cell(row, col=3, value="Да" if user.is_clicked_article else "Нет"),
                gspread.Cell(row, col=4, value="Да" if user.is_clicked_channel else "Нет"),
            ]
            row = row + 1

        self.worksheet_2.update_cells(result_cell)
        self.worksheet_2.format([f"A1:{self.last_header_a1_worksheet_2}"], {"textFormat": {"bold": True}})
        self.worksheet_2.format(
            [f"A1:{gspread.utils.rowcol_to_a1(result_cell[-1].row, result_cell[-1].col)}"],
            {"wrapStrategy": "WRAP", "verticalAlignment": "TOP"},
        )

    async def _init_worksheet_3(self) -> None:
        users_channel = await users_channel_db.get_users_channel(db_session)
        result_cell: list[gspread.Cell] = []

        # headers
        for col, header in enumerate(self.header_worksheet_3, 1):
            cell = gspread.Cell(row=1, col=col, value=header)
            result_cell.append(cell)

        row = 2
        for user_channel in users_channel:
            result_cell = result_cell + [
                gspread.Cell(
                    row, col=1, value=f"@{user_channel.username}" if user_channel.username else user_channel.first_name
                ),
                gspread.Cell(
                    row,
                    col=2,
                    value=user_channel.create_datetime.astimezone(tz=ZoneInfo("Europe/Moscow")).strftime(
                        "%d/%m/%Y, %H:%M:%S"
                    ),
                ),
            ]
            row = row + 1

        self.worksheet_3.update_cells(result_cell)
        self.worksheet_3.format([f"A1:{self.last_header_a1_worksheet_3}"], {"textFormat": {"bold": True}})
        self.worksheet_3.format(
            [f"A1:{gspread.utils.rowcol_to_a1(result_cell[-1].row, result_cell[-1].col)}"],
            {"wrapStrategy": "WRAP", "verticalAlignment": "TOP"},
        )

    async def update_table(self) -> None:
        try:
            await self._update_worksheet_1()
            await self._update_worksheet_2()
            await self._update_worksheet_3()
        except Exception as ex:
            log.exception(ex)

    async def _update_worksheet_1(self) -> None:
        answers_users = await answers_questions_db.get_results(db_session)
        row = 2
        result_cell: list[gspread.Cell] = []
        for col, header in enumerate(self.header_worksheet_1, 1):
            cell = gspread.Cell(row=1, col=col, value=header)
            result_cell.append(cell)

        for answers_user in answers_users:
            json_acceptable_string = answers_user.results.replace("'", '"')
            dict_value: dict[str, str] = json.loads(json_acceptable_string)

            result_cell = result_cell + [
                gspread.Cell(
                    row,
                    col=1,
                    value=f"@{answers_user.user.username}"
                    if answers_user.user.username
                    else answers_user.user.first_name,
                ),
                gspread.Cell(
                    row,
                    col=2,
                    value=answers_user.user.create_datetime.astimezone(tz=ZoneInfo("Europe/Moscow")).strftime(
                        "%d/%m/%Y, %H:%M:%S"
                    ),
                ),
            ]

            for col, answer in enumerate(dict_value.values(), 3):
                cell = gspread.Cell(row, col=col, value=answer)
                result_cell.append(cell)
            row = row + 1

        if result_cell:
            gs = gspread.auth.service_account(self.path_credits)
            table = gs.open_by_key(settings.GOOGLE_SHEET_TABLE_ID)
            worksheet_1 = table.worksheet("Лист1")
            worksheet_1.update_cells(result_cell)
            worksheet_1.format([f"A1:{self.last_header_a1_worksheet_1}"], {"textFormat": {"bold": True}})
            worksheet_1.format(
                [f"A1:{gspread.utils.rowcol_to_a1(result_cell[-1].row, result_cell[-1].col)}"],
                {"wrapStrategy": "WRAP", "verticalAlignment": "TOP"},
            )

    async def _update_worksheet_2(self) -> None:
        users = await users_db.get_users(db_session)
        result_cell: list[gspread.Cell] = []
        for col, header in enumerate(self.header_worksheet_2, 1):
            cell = gspread.Cell(row=1, col=col, value=header)
            result_cell.append(cell)

        row = 2
        for user in users:
            result_cell = result_cell + [
                gspread.Cell(row, col=1, value=f"@{user.username}" if user.username else user.first_name),
                gspread.Cell(
                    row,
                    col=2,
                    value=user.create_datetime.astimezone(tz=ZoneInfo("Europe/Moscow")).strftime("%d/%m/%Y, %H:%M:%S"),
                ),
                gspread.Cell(row, col=3, value="Да" if user.is_clicked_article else "Нет"),
                gspread.Cell(row, col=4, value="Да" if user.is_clicked_channel else "Нет"),
            ]
            row = row + 1

        if result_cell:
            gs = gspread.auth.service_account(self.path_credits)
            table = gs.open_by_key(settings.GOOGLE_SHEET_TABLE_ID)
            worksheet_2 = table.worksheet("Лист2")
            worksheet_2.update_cells(result_cell)
            worksheet_2.format([f"A1:{self.last_header_a1_worksheet_2}"], {"textFormat": {"bold": True}})
            worksheet_2.format(
                [f"A1:{gspread.utils.rowcol_to_a1(result_cell[-1].row, result_cell[-1].col)}"],
                {"wrapStrategy": "WRAP", "verticalAlignment": "TOP"},
            )

    async def _update_worksheet_3(self) -> None:
        users_channel = await users_channel_db.get_users_channel(db_session)
        result_cell: list[gspread.Cell] = []

        # headers
        for col, header in enumerate(self.header_worksheet_3, 1):
            cell = gspread.Cell(row=1, col=col, value=header)
            result_cell.append(cell)

        row = 2
        for user_channel in users_channel:
            result_cell = result_cell + [
                gspread.Cell(
                    row, col=1, value=f"@{user_channel.username}" if user_channel.username else user_channel.first_name
                ),
                gspread.Cell(
                    row,
                    col=2,
                    value=user_channel.create_datetime.astimezone(tz=ZoneInfo("Europe/Moscow")).strftime(
                        "%d/%m/%Y, %H:%M:%S"
                    ),
                ),
            ]
            row = row + 1

        if result_cell:
            gs = gspread.auth.service_account(self.path_credits)
            table = gs.open_by_key(settings.GOOGLE_SHEET_TABLE_ID)
            worksheet_3 = table.worksheet("Лист3")
            worksheet_3.update_cells(result_cell)
            worksheet_3.format([f"A1:{self.last_header_a1_worksheet_2}"], {"textFormat": {"bold": True}})
            worksheet_3.format(
                [f"A1:{gspread.utils.rowcol_to_a1(result_cell[-1].row, result_cell[-1].col)}"],
                {"wrapStrategy": "WRAP", "verticalAlignment": "TOP"},
            )
