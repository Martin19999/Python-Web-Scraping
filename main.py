from bs4 import BeautifulSoup
import requests
import csv

module_info_csv = open('NL_modules_info.csv', 'w')
csv_writer = csv.writer(module_info_csv)
csv_writer.writerow(['Title', 'Link', 'Semester', 'Credits', 'Comments',
                     'Assessment_1', 'Timing_1', 'Open Book Exam_1', 'Component Scale_1', 'Must Pass_1', 'Percentage_1',
                     'Assessment_2', 'Timing_2', 'Open Book Exam_2', 'Component Scale_2', 'Must Pass_2', 'Percentage_2',
                     'Assessment_3', 'Timing_3', 'Open Book Exam_3', 'Component Scale_3', 'Must Pass_3', 'Percentage_3',
                     'Assessment_4', 'Timing_4', 'Open Book Exam_4', 'Component Scale_4', 'Must Pass_4', 'Percentage_4',
                     'Assessment_5', 'Timing_5', 'Open Book Exam_5', 'Component Scale_5', 'Must Pass_5', 'Percentage_5'])

# the home page that includes every module.
# a request object.text
homePageHtmlFile = requests.get("https://www.ucd.ie/cs/study/postgraduate/nlthemes/").text
homePage = BeautifulSoup(homePageHtmlFile, "lxml")

# [module title] = [url, semester 1/2, credits, comments]
module_mainPage_info = []
for moduleTitle in homePage.findAll('tr'):
    if moduleTitle.td is not None:
        if moduleTitle.td.a is not None:
            tds = moduleTitle.findAll('td')
            module_mainPage_info.append([tds[0].a.text, tds[0].a['href'], tds[1].text, tds[2].text,
                                        tds[3].text if tds[3].text != '\xa0' else ""])

assessment_info = []

# for every module
for i, info1 in enumerate(module_mainPage_info):
    secondPageHtmlFile = requests.get(info1[1]).text
    secondPage = BeautifulSoup(secondPageHtmlFile, "lxml")
    # "sections" includes: How will I be assessed? When is this module offered? etc.
    sections = secondPage.findAll('section', class_='panel panel-default')

    assessment_info_for_one_module = []

    for section in sections:
        panel_heading = section.find('div', role='tab')
        panel_heading_text = panel_heading.a.text.strip()
        if panel_heading_text == "How will I be assessed?":  # this is the section "How will I be assessed?"
            panel_body = section.find('div', role='tabpanel')
            target_rows = panel_body.table.tbody
            elements = target_rows.findAll('td')
            for ele in elements:
                module_mainPage_info[i].append(ele.text)
                assessment_info_for_one_module.append(ele.text)

    assessment_info.append(assessment_info_for_one_module)
    print(assessment_info_for_one_module)

print(module_mainPage_info)

for elements in module_mainPage_info:
    csv_writer.writerow(elements)

module_info_csv.close()
