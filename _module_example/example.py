from extensions import ModuleBase
from extensions import single_chat

# 단일채팅 응답 모듈 예시

# run 메소드에 single_chat 데코레이터를 적용하면
# 문자열 하나만 리턴하도록 짤 수 있음

class Module(ModuleBase):
    commands = ["카운터"]

    # 봇 처음 작동시에만 실행됨
    def __init__(self):
        self.count = {}

    @single_chat
    def run(self, params, usr_i):
        assert params[0] == "!봇"
        assert params[1] == "카운터"

        if len(params) != 3:
            return "example.py: 사용법\n" \
                   "!봇 카운터 [올릴숫자]"
        else:
            try:
                num = int(params[2])
            except:
                return "example.py: 사용법\n" \
                       "!봇 카운터 [올릴숫자]"

            if usr_i not in self.count:
                self.count[usr_i] = num
            else:
                self.count[usr_i] += num
            
            return f"{usr_i} 카운터값: {self.count[usr_i]}"



