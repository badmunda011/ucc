import random
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

CHAT_STORAGE = [
    "mongodb+srv://BADMUNDA:BADMYDAD@badhacker.i5nw9na.mongodb.net/",
    "mongodb+srv://SUKH:BAD@badmunda.flyudhy.mongodb.net/",
    "mongodb+srv://Badmunda_13:badmunda50@cluster0.9oyzqux.mongodb.net/",
]

BADMUNDA = MongoCli(random.choice(CHAT_STORAGE))
chatdb = BADMUNDA.Anonymous
chatai = chatdb.Word.WordDb
storeai = BADMUNDA.Anonymous.Word.NewWordDb  
