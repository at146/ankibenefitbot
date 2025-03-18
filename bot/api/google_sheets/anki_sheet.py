import json
import uuid

import gspread

from bot.core.config import settings
from bot.crud.answers_questions_db import get_results
from bot.crud.users_db import get_users
from bot.db.session import db_session
from bot.dialogs.menu.questioning.text import DICT_QUESTIONS, LAST_QUESTION
from bot.init import log


class AnkiSheet:
    def __init__(self, path_credits: str) -> None:
        self.path_credits = path_credits
        self.gs = gspread.auth.service_account(self.path_credits)
        # подключаем таблицу по ID
        self.table = self.gs.open_by_key(settings.GOOGLE_SHEET_TABLE_ID)

    async def init_table(self) -> None:
        # TODO: batch_format, format
        await self._init_worksheet_1()
        await self._init_worksheet_2()

    async def _init_worksheet_1(self) -> None:
        answers_users = await get_results(db_session)
        result_cell: list[gspread.Cell] = []

        header_list = ["Ник ТГ", "Дата и Время входа"]
        for value in DICT_QUESTIONS.values():
            header_list.append(value["question"])  # type: ignore
        header_list.append(LAST_QUESTION["question"])  # type: ignore

        for col, header in enumerate(header_list, 1):
            cell = gspread.Cell(row=1, col=col, value=header)
            result_cell.append(cell)

        answers_users = await get_results(db_session)

        # вероятность очень мала))
        random_str = uuid.uuid4().hex
        self.worksheet_1 = self.table.add_worksheet(random_str, rows=0, cols=0, index=0)

        worksheets = self.table.worksheets()
        for ws in worksheets:
            if ws.index != 0:
                self.table.del_worksheet(ws)

        self.worksheet_1.update_title("Лист1")

        self.worksheet_2 = self.table.add_worksheet("Лист2", rows=0, cols=0, index=1)

        row = 2
        for answers_user in answers_users:
            json_acceptable_string = answers_user.results.replace("'", '"')
            dict_value: dict[str, str] = json.loads(json_acceptable_string)
            result_cell = result_cell + [
                gspread.Cell(row, col=1, value=answers_user.user.username or ""),
                gspread.Cell(row, col=2, value=answers_user.user.create_datetime.strftime("%d/%m/%Y, %H:%M:%S")),
            ]
            for col, answer in enumerate(dict_value.values(), 3):
                cell = gspread.Cell(row, col=col, value=answer)
                result_cell.append(cell)
            row = row + 1

        self.worksheet_1.update_cells(result_cell)

    async def _init_worksheet_2(self) -> None:
        users = await get_users(db_session)
        result_cell: list[gspread.Cell] = []
        header_list = ["Ник ТГ", "Дата и Время входа", "Забрал статью", "Перешел в канал"]

        for col, header in enumerate(header_list, 1):
            cell = gspread.Cell(row=1, col=col, value=header)
            result_cell.append(cell)

        row = 2
        for user in users:
            result_cell = result_cell + [
                gspread.Cell(row, col=1, value=user.username or ""),
                gspread.Cell(row, col=2, value=user.create_datetime.strftime("%d/%m/%Y, %H:%M:%S")),
                gspread.Cell(row, col=3, value="Да" if user.is_clicked_article else "Нет"),
                gspread.Cell(row, col=4, value="Да" if user.is_clicked_channel else "Нет"),
            ]
            row = row + 1

        self.worksheet_2.update_cells(result_cell)

    async def update_table(self) -> None:
        try:
            await self._update_worksheet_1()
            await self._update_worksheet_2()
        except Exception as ex:
            log.exception(ex)

    async def _update_worksheet_1(self) -> None:
        answers_users = await get_results(db_session)
        row = 2
        result_cell: list[gspread.Cell] = []
        for answers_user in answers_users:
            json_acceptable_string = answers_user.results.replace("'", '"')
            dict_value: dict[str, str] = json.loads(json_acceptable_string)

            result_cell = result_cell + [
                gspread.Cell(row, col=1, value=answers_user.user.username or ""),
                gspread.Cell(row, col=2, value=answers_user.user.create_datetime.strftime("%d/%m/%Y, %H:%M:%S")),
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

    async def _update_worksheet_2(self) -> None:
        users = await get_users(db_session)
        result_cell: list[gspread.Cell] = []
        header_list = ["Ник ТГ", "Дата и Время входа", "Забрал статью", "Перешел в канал"]

        for col, header in enumerate(header_list, 1):
            cell = gspread.Cell(row=1, col=col, value=header)
            result_cell.append(cell)

        row = 2
        for user in users:
            result_cell = result_cell + [
                gspread.Cell(row, col=1, value=user.username or ""),
                gspread.Cell(row, col=2, value=user.create_datetime.strftime("%d/%m/%Y, %H:%M:%S")),
                gspread.Cell(row, col=3, value="Да" if user.is_clicked_article else "Нет"),
                gspread.Cell(row, col=4, value="Да" if user.is_clicked_channel else "Нет"),
            ]
            row = row + 1

        if result_cell:
            gs = gspread.auth.service_account(self.path_credits)
            table = gs.open_by_key(settings.GOOGLE_SHEET_TABLE_ID)
            worksheet_2 = table.worksheet("Лист2")
            worksheet_2.update_cells(result_cell)
