command = ["이미지1", "이미지2"]

IMG_PREFIX = "REQUETST_IMAGE_"

def Com(params, usr_i):
    bot_name = params[0]         # "!봇"
    module_name = params[1]      # "이미지1 or 이미지2"
    user_name = usr_i

    param_num = len(params)

    if param_num == 3:
        # sample_images/image1.jpg를 전송
        if params[1] == "이미지1":
            return IMG_PREFIX + "sample_images/folder1/image1.jpg"
        
        # sample_images/image2.jpg를 전송
        elif params[1] == "이미지2":
            return IMG_PREFIX + "sample_images/folder2/image2.jpg"
        
        # image1과 image2를 연속으로 전송: 개행문자로 구분
        elif params[1] == "이미지12":
            response =  IMG_PREFIX + "sample_images/folder1/image1.jpg\n" 
            response += IMG_PREFIX + "sample_images/folder2/image2.jpg"
            return response

        # 이론상 호출될 일 없음.
        else:
            return "image.py: 잘못된 명령어 사용"

    else:
        return "image.py: 사용법:\n"\
            "!봇 이미지1\n!봇 이미지2\n!봇 이미지12"
