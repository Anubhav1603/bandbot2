from extensions import ModuleBase

# image 및 다중명령어 모듈 예시

# commands가 리스트이므로 여러 명령어를 지원할 수 있음.
# 이미지 상대경로는 start.py가 위치한 프로젝트 루트 기준.

class Module(ModuleBase):
    commands = ["이미지1", "이미지2"]

    def run(self, params, usr_i):
        assert params[0] == "!봇"
        assert params[1] in Module.commands

        if len(params) != 2:
            return [("chat", "example.py: 사용법\n!봇 [이미지1|이미지2]")]
        else:
            if params[1] == "이미지1":
                return [("image", "module_example/sample_images/folder1/image1.jpg")]
            elif params[1] == "이미지2":
                return [("image", "module_example/sample_images/folder1/image2.jpg")]