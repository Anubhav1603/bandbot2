from mcstatus import MinecraftServer

from extensions import ModuleBase
from extensions import single_chat

from socket import gaierror

class Module(ModuleBase):
    commands = ["마크서버"]

    @single_chat
    def run(self, params, usr_i):
        paramnum = len(params)

        if paramnum != 3:
            return "mcserver.py: 사용법\n!봇 마크서버 [주소]"

        addr = params[2]
        server = MinecraftServer.lookup(addr)

        try:
            status = server.status()
            players = status.players.online
            return f"{addr} 온라인\n{players}명 접속중"
        except ConnectionRefusedError as e:
            print(e)
            return "mcserver.py: 서버가 꺼져있습니다."
        except gaierror as e:
            print(e)
            return "mcserver.py: 잘못된 주소입니다."
        