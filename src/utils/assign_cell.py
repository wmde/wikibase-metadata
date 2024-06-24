def assign_cell(
    worksheet, x: int, y: int, value: bool | int | float | str, overwrite: bool = False
) -> None:
    c = worksheet.cell(y, x)
    if c.value is None or overwrite:
        c.value = value
