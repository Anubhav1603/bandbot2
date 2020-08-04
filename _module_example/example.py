command = ["에코", "이미지1", "이미지12"]

IMG_PREFIX = "REQUETST_IMAGE_"

def Com(params, usr_i):
    bot_name = params[0]            # !봇
    module_name = params[1]         # 에코, 이미지1, 이미지12
    user_name = usr_i               # 호출 유저 닉네임

    guide = "example.py: 사용법:\n"\
            "!봇 에코 [문자열]\n!봇 이미지1\n!봇 이미지12"
    
    param_num = len(params)

    if module_name == "에코":
        if param_num == 3:
            return user_name + ":" + params[2]
        else:
            return guide
    
    # sample_images/image1.jpg를 전송
    elif module_name == "이미지1":
        if param_num == 2:
            img_path = "module_example/sample_images/folder1/image1.jpg"
            return IMG_PREFIX + img_path
        else:
            return guide
    
    # image1과 image2를 연속으로 전송: 개행문자로 구분
    elif module_name == "이미지12":
        if param_num == 2:
            response = ""
            img_path_1 = "module_example/sample_images/folder1/image1.jpg"
            img_path_2 = "module_example/sample_images/folder2/image2.jpg"
            response += IMG_PREFIX + img_path_1 + "\n"
            response += IMG_PREFIX + img_path_2
        else:
            return guide