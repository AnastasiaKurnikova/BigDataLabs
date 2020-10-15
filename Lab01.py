import pandas as pd 

print('1) Считывание данных:')
data = pd.read_csv('brooklyn_sales_map.csv', sep = ',')


print('2) Запись данных:')
Search = data['building_class_category'].unique()
#print(Search)
for i in Search:
    SearchResult = data.loc[data['building_class_category'] == i]
    SearchResult.to_csv(str(i).replace("/","-") + '.csv')
 
    
print('3) Вычисления: ')  
Name = data.select_dtypes(include='number').columns
#print(Name)
for i in Name:
    print('Название столбца: ' + i)
    print('Количество пропущенных значений: ' + str(data[i].isna().sum()))
    print('Cреднее значение:' + str(data[i].mean()))
    print('Медиана:' + str(data[i].median()))
    print('Наибольшее значение:' + str(data[i].max()))
    print('Наименьшее значение:' + str(data[i].min()))
    print('Количество уникальных значений:' + str(len(data[i].unique())))
    print('\n' + '__________' + '\n')

    
print('4) Доля от всей выборки: ')     
for i in Search:
    try:
        share=data['building_class_category'].value_counts()[i]/len(data['building_class_category'].values)
        print('Доля значения поля '+ i + ' = ' + str(share))
    except:
        continue

    
print('5)Нормализация данных:')    
norm = (data._get_numeric_data() - data._get_numeric_data().min())/(data._get_numeric_data().max() - data._get_numeric_data().min())
print(norm)