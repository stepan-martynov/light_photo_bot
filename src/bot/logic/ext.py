


async def print_state_data(msg: str, userdata: dict, filter: tuple = ()) -> str:
    str = msg + "\n"
    for key, value in userdata.items():
        if filter and key not in filter:
            continue
        str += f"{key}: {value}\n"
    return str
