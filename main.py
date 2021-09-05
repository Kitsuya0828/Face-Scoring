import requests
import base64
from collections import defaultdict
import glob
from scraping import scrape

endpoint = 'https://api-us.faceplusplus.com'

# 1:Male, 0:Female
people = [
    ['大谷翔平', 'ohtanishohei', 1],
]

average_scores = defaultdict(float)

for person in people:

    keyword = person[0]
    dir_name = person[1]
    gender = "male" if person[2] else "female"

    scrape(keyword, dir_name)

    src = sorted(glob.glob(f'picture/{dir_name}/*.jpg'))

    scores = []

    for i, file in enumerate(src):
        # print(f"{i}:{file}")
        img_file = base64.b64encode(open(file, 'rb').read())
        response = requests.post(
            endpoint + '/facepp/v3/detect',
            {
                'Content-Type': 'multipart/form-data',
                'api_key': "{your_api_key}",
                'api_secret': "{your_api_secret}",
                'image_base64': img_file,
                'return_attributes': 'gender,age,headpose,facequality,eyestatus,emotion,ethnicity,beauty,mouthstatus'
            }
        )

        try:
            result = response.json()

            if len(result["faces"]) != 1:   # 顔は１つだけ
                continue
            if result["faces"][0]["attributes"]["mouthstatus"]["surgical_mask_or_respirator"] >= 90:    # マスクNG
                continue
            if result["faces"][0]["attributes"]["glass"]["value"] == "Dark":    # サングラスNG
                continue
            if result["faces"][0]["attributes"]["eyestatus"]["left_eye_status"]["occlusion"] >= 90 or result["faces"][0]["attributes"]["eyestatus"]["right_eye_status"]["occlusion"] >= 90:   # 最低片目が映る
                continue
            if result["faces"][0]["attributes"]["eyestatus"]["left_eye_status"]["no_glass_eye_close"] >= 90 or result["faces"][0]["attributes"]["eyestatus"]["right_eye_status"]["no_glass_eye_close"] >= 90:   # 最低片目開いてる
                continue
            if result["faces"][0]["attributes"]["eyestatus"]["left_eye_status"]["normal_glass_eye_close"] >= 90 or result["faces"][0]["attributes"]["eyestatus"]["right_eye_status"]["normal_glass_eye_close"] >= 90:   # 最低片目開いてる
                continue
            if result['faces'][0]['face_rectangle']['top'] <= -55:  # 顔の目より上がフレーム内
                continue
            score = result["faces"][0]["attributes"]['beauty'][f'{gender}_score']
            print(f'score = {score}')

            if score <= 40:
                continue

            scores.append(score)

        except Exception as e:
            print(e)
            print(f"{i}:{file}でエラーが発生")
    print(f'average score = {sum(scores)/len(scores)}')
    average_scores[keyword] = sum(scores)/len(scores)

for k,v in average_scores.items():
    print(f'{k} : {v}', )