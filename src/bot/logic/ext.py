


async def print_userdata(userdata: dict, filter: tuple) -> str:
    str = "\n"
    for key, value in userdata.items():
        if key in filter:
            str += f"{key}: {value}\n"
    return str
