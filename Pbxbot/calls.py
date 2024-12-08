from Pbxbot.core.clients import Pbxbot
from pytgcalls import PyTgCalls, filters as pytgfl
from pytgcalls.types import ChatUpdate, Update, GroupCallConfig
from pytgcalls.types import Call, MediaStream, AudioQuality, VideoQuality


call = PyTgCalls(Pbxbot)
call_config = GroupCallConfig(auto_start=False)
