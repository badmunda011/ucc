from Pbxbot.core import Config
from typing import Dict, List, Union, Callable


admins: Dict[int, List[int]] = {}


def set_admins(chat_id: int, admins_: List[int]):
    admins[chat_id] = admins_


def get_admins(chat_id: int) -> Union[List[int], bool]:
    return admins.get(chat_id, False)


async def get_administrators(chat) -> List[int]:
    get = get_admins(chat.id)

    if get:
        return get
    else:
        administrators = chat.get_members(filter="administrators")
        to_set = []

        for administrator in administrators:
            if administrator.can_manage_voice_chats:
                to_set.append(administrator.user.id)

        set_admins(chat.id, to_set)
        return await get_administrators(chat)




def authorized_users(func: Callable) -> Callable:
    async def decorator(client, message):
        if message.from_user.id in STAN_USERS:
            return await func(client, message)

        administrators = await get_administrators(message.chat)

        for administrator in administrators:
            if administrator == message.from_user.id:
                return await func(client, message)

    return decorator


