from openpyxl import Workbook

from src.project_constants import URL_FILENAME, URL_MASTER_LIST
from src.utils.assign_cell import assign_cell


def create_url_sheet(wb: Workbook):
    ws = wb.active
    ws.title = "URLS"

    assign_cell(ws, 1, 1, "URL")
    assign_cell(ws, 2, 1, "Action Query API")
    assign_cell(ws, 3, 1, "SPARQL Query Page")
    assign_cell(ws, 4, 1, "SPARQL Endpoint")
    assign_cell(ws, 5, 1, "Index Query API")

    for i, url in enumerate(URL_MASTER_LIST):
        assign_cell(ws, 1, i + 2, url)
        assign_cell(ws, 2, i + 2, url + "/w/api.php")
        assign_cell(ws, 4, i + 2, url + "/proxy/wdqs/bigdata/namespace/wdq/sparql")
        assign_cell(ws, 5, i + 2, url + "/w/index.php")

    wb.save(URL_FILENAME)
