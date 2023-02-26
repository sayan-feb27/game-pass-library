import json

import pygsheets as pygs
from pygsheets.client import Client


class GoogleSpreadSheetParser:
    def __init__(
        self,
        *,
        service_file: str,
        spread_sheet_url: str,
        headers_row_index: int = 1,
        output_path: str = "./gs_results.json"
    ):
        self.spread_sheet_url = spread_sheet_url
        self.headers_row_index = headers_row_index
        self.output_path = output_path
        self.gclient: Client = pygs.authorize(service_file=service_file)

    def parse(self):
        sheet: pygs.Spreadsheet = self.gclient.open_by_url(self.spread_sheet_url)
        first_ws: pygs.Worksheet = sheet.sheet1
        raw_rows = first_ws.get_all_records(head=self.headers_row_index)

        with open(self.output_path, "w") as file:
            json.dump(raw_rows, file)


if __name__ == "__main__":
    import argparse

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("url", help="url of a spreadsheet to parse")
    arg_parser.add_argument(
        "--service-file",
        dest="service_file",
        default="./credentials.json",
        help="path a file with your google credentials",
    )
    arg_parser.add_argument("--header-row", type=int, default=1, dest="header_row")
    arg_parser.add_argument(
        "-o", "--output-to", dest="output_path", default="./gs_results.json"
    )

    args = arg_parser.parse_args()

    parser = GoogleSpreadSheetParser(
        service_file=args.service_file,
        headers_row_index=args.header_row,
        spread_sheet_url=args.url,
        output_path=args.output_path,
    )
    parser.parse()
