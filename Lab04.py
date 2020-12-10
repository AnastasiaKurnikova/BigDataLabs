import pandas
import re
import csv
import dateutil.parser
import datetime

DF = pandas.read_csv("Vacancies.csv", delimiter = ",", index_col = [0], na_values = ['NA'], low_memory = False)

delimiters = ['/','+',' ']

comb = ['c++','c#','php','asp.net','ui','ux','qt','sql','delphi','vuejs','angular','unix','linux','java','typescript','win','kotlin','golang','python','node.js','backend','frontend','junior', 'middle', 'senior','go','html5','html','reactjs','ios','android']

variants = [
        ['frontend', 'front-end', 'front end', 'фронтенд', 'фронтэндер'],
        ['backend', 'back-end', 'back end', 'бэкенд'],
        ['developer', 'разработчик'],
        ['programmer', 'программист'],
        ['game designer', 'гейм дизайнер', 'геймдизайнер'],
        ['designer', 'дизайнер'],
        ['copywriter', 'копирайтер'],
        ['manager', 'менеджер'],
        ['animator', 'аниматор'],
        ['artist', 'художник'],
        ['middle','миддл'],
        ['js', 'javascript'],
        ['web','вэб'],
        ['teamlead','тимлид', 'team lead', 'team leader'],
        ['devops', 'девопс'],
        ['fullstack','full стек','full-стек','full stack'],
        ['бд','баз данных','баз даных','базы данных'],
        ['2d','2д'],
        ['3d','3д'],
        ['bitrix','битрикс'],
        ['analyst','аналитик'],
        ['big data','bigdata'],
        ['tech lead','techlead'],
        ['mssql','ms sql'],
        ['presale','pre sale', 'presales', 'pre sales']
    ]

Del = ['удаленно','remote','full-time','full time','фултайм','fulltime', '(\(.*\))','(\[.*\])','\s+в\s+.*','г\.\s+.*']

print("Замена знаков:")

DF["Name"] = DF["Name"].apply(lambda x: x.lower())
DF["Name"] = DF["Name"].apply(lambda x: x.replace('\\','/'))
DF["Name"] = DF["Name"].apply(lambda x: x.replace('|','/'))
DF["Name"] = DF["Name"].apply(lambda x: x.replace(',','/'))
DF["Name"] = DF["Name"].apply(lambda x: x.replace('-',' '))
DF["Name"] = DF["Name"].apply(lambda x: re.sub('\s*\/\s*', '/', x))
DF["Name"] = DF["Name"].apply(lambda x: re.sub('\s+', ' ', x).strip())

print("Удаление слов:")

for d in Del:
    regex = re.compile(d)
    DF["Name"] = DF["Name"].apply(lambda x: regex.sub('', x))

print("Замена слов:")

for v in variants:
    for i in range(1, len(v)):
        DF["Name"] = DF["Name"].apply(lambda x: x.replace(v[i],v[0]))

print("Перестановка различных вариантов в названии:")

for i in range(len(comb)):
    for j in range(i+1, len(comb)):
        for d in delimiters:
            regex = re.compile(re.escape(comb[j])+'\s*'+re.escape(d)+'\s*'+re.escape(comb[i]))
            DF["Name"] = DF["Name"].apply(lambda x: regex.sub(comb[i]+delimiters[0]+comb[j], x))

DF["Name"] = DF["Name"].apply(lambda x: re.sub('\s+', ' ', x).strip())

print("Замена пустых значений:")

DF["Employer name"] = DF["Employer name"].fillna("Не указано")
DF["City"] = DF["City"].fillna("Не указан")
DF["Expierence"] = DF["Expierence"].fillna("Не требуется")
DF["Employment"] = DF["Employment"].fillna("Любой тип")
DF["Schedule"] = DF["Schedule"].fillna("Любой график")
DF["Responsibility"] = DF["Responsibility"].fillna("Нету")
DF["Requirement"] = DF["Requirement"].fillna("Нету")
DF["Key skills"] = DF["Key skills"].fillna("Нету")

DF["Salary from"] = DF.groupby(["Name", "City"]).transform(lambda x: x.fillna(x.mean()))["Salary from"]
DF["Salary to"] = DF.groupby(["Name", "City"]).transform(lambda x: x.fillna(x.mean()))["Salary to"]

print("Добавление дней:")

DF["Published at"] = DF["Published at"].apply(lambda x: (datetime.datetime.now() - dateutil.parser.parse(x).replace(tzinfo=None)).days)

print("Запись в .csv:")

DF.to_csv("Result.csv",  na_rep = 'NA', index = True, index_label = "", quotechar = '"', quoting = csv.QUOTE_NONNUMERIC, encoding = "utf-8-sig")
