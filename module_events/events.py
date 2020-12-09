from API.princess import Event, PrincessError

from extensions import ModuleBase, single_chat

class Module(ModuleBase):
    commands = ["밀리이벤", "밀리이벤컷"]

    @single_chat
    def run(self, params, usr_i):
        try:
            if params[1] == '밀리이벤':
                event = Event()
                return event.get_info_formatted()
            elif params[1] == '밀리이벤컷':
                event = Event()
                return event.get_cut_formatted()
            else:
                return "events.py: 잘못된 명령어"

        except PrincessError as e:
            print(e)
            return "events.py: " + str(e)

        except Exception as e:
            print(e)
            return "events.py: 처리되지 않은 예외"