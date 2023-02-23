from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
# import logging
# import csv
# logging.basicConfig(
#     filename='Assignment_Youtube_Scrapper.log', level=logging.INFO)
# creation of api's goes here:

app = Flask(__name__)


@app.route("/", methods=['GET'])
@cross_origin()
def home_page():
    # return render_template('index.html')
    return render_template('index.html')


@app.route("/result", methods=['GET', 'POST'])
@cross_origin()
def result():
    links = []
    thumbnails = []
    views = []
    time = []
    titles = []
    if request.method == 'POST':
        # Here should go my scrapping logic.
        Assignment_url = request.form['content']
        driver = webdriver.Chrome()
        driver.get(Assignment_url)
        user_data = driver.find_elements(
            "xpath", '//*[@id="video-title-link"]')
        views_data = driver.find_elements(
            "xpath", '//*[@id="metadata-line"]/span[1]')
        time_data = driver.find_elements(
            "xpath", '//*[@id="metadata-line"]/span[2]')
        url_thumbnails = driver.find_elements(
            'xpath', '//*[@id="thumbnail"]/yt-image/img')
        # //*[@id = "thumbnail"]/yt-image/img
        for i in url_thumbnails:
            txt = i.get_attribute('src')
            # print(txt)
            thumbnails.append(txt)
            if (len(thumbnails) == 5):
                break

        for i in user_data:
            links.append(i.get_attribute('href'))
            # print(i.get_attribute('title'))
            titles.append(i.get_attribute('title'))
            if (len(links) == 5):
                break
            # print(i.get_attribute('href'))
        for i in views_data:
            # print(i.text)
            views.append(i.text)
            if (len(views) == 5):
                break
        for i in time_data:
            # print(i.text)
            time.append(i.text)
            if (len(time) == 5):
                break
    collection = list()
    for i in range(0, 5):
        dict = {}
        dict['link'] = links[i]
        if (thumbnails[i] == None):
            dict['thumbnail'] = 'Unable to fetch Thumbnail URL!!'
        else:
            dict['thumbnail'] = thumbnails[i]
        dict['title'] = titles[i]
        dict['view'] = views[i]
        dict['time'] = time[i]
        collection.append(dict)
    # header = ['video link', 'thumbnail Link', 'title', 'view', 'time']
    # # Code To create csv file.
    # with open('youtube_details.csv', 'w', encoding='UTF8', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(header)
    #     for i in collection:
    #         data = list()
    #         data.append(i['link'])
    #         data.append(i['thumbnail'])
    #         data.append(i['title'])
    #         data.append(i['view'])
    #         data.append(i['time'])
    #         writer.writerow(data)

    return render_template('result.html', collection=collection)


if __name__ == "__main__":
    app.run(host="0.0.0.0")


# scraping logic.


# df = pd.DataFrame(columns=['link', 'title'])
# # url of video thumbnails, title of videos, views of videos, time of posting of video
# wait = WebDriverWait(driver, 10)
# for x in links:
#     driver.get(x)
#     v_id = x.strip("https://www.youtube.com/watch?v=")
#     v_title = wait.until(EC.presence_of_element_located(
#         (By.CSS_SELECTOR, "h1.title yt-formatted-string"))).text
#     print(v_title)
#     df.loc[len(df)] = [v_id, v_title]
