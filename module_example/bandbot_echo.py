command = ["에코", "에코두번"]

def Com(params, usr_i):
    bot_name = params[0]         # "!봇"
    module_name = params[1]      # "에코 or 에코두번"
    user_name = usr_i
    
    param_num = len(params)

    if param_num == 3:
        if params[1] == "에코":
            return user_name + ":" + params[2]
        elif params[1] == "에코두번":
            return user_name + ":" + params[2] * 2
        else:
            # 이론상 호출될 일 없음.
            return "echo.py: 잘못된 명령어 사용"
    else:
        return "sample.py: 사용법:\n"\
            "!봇 에코 [문자열]\n!봇 에코두번 [문자열]"


"""
ㅎㅅㅋ: !봇 에코 테스트
응답: [밴드봇] ㅎㅅㅋ
      ㅎㅅㅋ:테스트

ㅎㅅㅋ: !봇 에코두번 테스트
응답: [밴드봇] ㅎㅅㅋ
      ㅎㅅㅋ:테스트테스트

ㅎㅅㅋ: !봇 에코
응답: [밴드봇] ㅎㅅㅋ
      sample.py: 사용법:
      !봇 에코 [문자열]
      !봇 에코두번 [문자열]

ㅎㅅㅋ: !봇 에코 테스트 테스트
응답: [밴드봇] ㅎㅅㅋ
      sample.py: 사용법:
      !봇 에코 [문자열]
      !봇 에코두번 [문자열]
"""