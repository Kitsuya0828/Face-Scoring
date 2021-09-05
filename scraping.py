from google_images_download import google_images_download
import glob
import os

def scrape(keyword, dir_name):
    config = {
        "Records": [
            {
                "keywords": keyword,
                "no_numbering": True,
                "limit": 100,
                "output_directory": "picture",
                "image_directory": dir_name,
                "chromedriver": "{your_chromedriver_path}",
            }
        ]
    }

    response = google_images_download.googleimagesdownload()
    for rc in config["Records"]:
        response.download(rc)

    gifImgs = glob.glob("picture" + os.sep + "*" + os.sep + "*.gif")
    # print(f"removing gif files: {len(gifImgs)} files")
    _ = [os.remove(f) for f in gifImgs]

# scrape("阿部寛",'abehiroshi')