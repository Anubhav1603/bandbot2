from extensions import ModuleBase

# delay기능 및 다중채팅 응답 모듈 예시

# 여러개의 문자열을 리턴하거나
# delay, image, change등 고급기능을 사용하면
# single_chat 데코레이터를 사용할 수 없음.

class Module(ModuleBase):
    commands = ["고오급개그"]

    def run(self, params, usr_i):
        assert params[0] == "!봇"
        assert params[1] == "고오급개그"

        if len(params) != 2:
            return [("chat", "example.py: 사용법\n!봇 고오급개그")]
        else:
            res1 = ("chat", "비빔면 비빌때 팔을 조심해야하는 이유는?")
            res2 = ("delay", "3.2")         # 3.2초 딜레이
            res3 = ("chat", "팔도 비빔면 되니까")
            res4 = ("chat", "엌ㅋㅋㅋㅋㅋㅋ")
            return [res1, res2, res3, res4]