import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

data = pd.read_csv('data.csv')

st.write('**Графики распределения признаков**')

# Боксплоты
box_column = st.selectbox(
     'Выберите признак для построения boxplot',
     ('AGE', 'PERSONAL_INCOME'))

fig, ax = plt.subplots()
ax.boxplot(data[box_column])
plt.grid()
plt.title(box_column)
st.pyplot(fig)
st.write('Выбросов нет')


st.divider()
# Гистограммы
hist_column = st.selectbox(
     'Выберите признак для построения гистограммы',
     ('AGE', 'PERSONAL_INCOME'))

fig, ax = plt.subplots()
if hist_column == 'PERSONAL_INCOME':
     ax.hist(data[hist_column], bins=20)
else:
     ax.hist(data[hist_column], bins=data[hist_column].nunique())
plt.grid()
plt.title(hist_column)
st.pyplot(fig)


st.divider()
# Барплоты
bar_column = st.selectbox(
     'Выберите признак для построения barplot',
     ('TARGET', 'SOCSTATUS_WORK_FL', 'SOCSTATUS_PENS_FL', 'GENDER',
       'CHILD_TOTAL', 'DEPENDANTS', 'LOAN_NUM_TOTAL', 'LOAN_NUM_CLOSED'))

bar_data = data[bar_column].value_counts().sort_index().to_dict()
vals = list(map(str, bar_data.keys()))
cnts = bar_data.values()

fig, ax = plt.subplots()
ax.bar(vals, cnts)
plt.grid()
plt.title(bar_column)
st.pyplot(fig)
st.write('Большая часть клинтов в настоящий момент работают')
st.write('Мужчин примерно в 2 раза больше женщин')
st.write('Большинство опрашиваемы имеют до вдух детей. Пимерно у трети детей нет')
st.write('Примерно у половины опрашиваемых нет иждивенцев')
st.write('Большая часть ссуд не погашены')


st.divider()
st.write('**Матрица корреляций**')
# Коррелограмма
corr_df = data.drop('AGREEMENT_RK', axis=1)
fig, ax = plt.subplots()
fig.set_figheight(15)
fig.set_figwidth(20)
sns.heatmap(corr_df.corr(), xticklabels=corr_df.corr().columns, yticklabels=corr_df.corr().columns, cmap='RdYlGn', center=0, annot=True)
plt.title('Коррелограмма', fontsize=50)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
st.pyplot(fig)
st.write('Между целевой и другими признаками не наблюдается сильной линейной зависимости')
st.write('Количество погашенных ссуд и общее количествоо ссуд имеют сильную положительную корреляцию')
st.write('Возраст и статус пенсионера, а так же количество детей и количество иждевенцев имеют умеренную прямую зависимость')
st.write('Признаки отвечающие за работу и пенсию имеют выскую обратную корреляцию')


st.divider()
st.write('**Графики зависимостей целевой переменной и признаков**')
# Графики зависимостей целевой переменной и признаков
compare_column = st.selectbox(
     'Выберите признак для построения графика зависимости с целевой',
     ('AGE', 'SOCSTATUS_WORK_FL','SOCSTATUS_PENS_FL', 'GENDER', 'CHILD_TOTAL',
       'DEPENDANTS', 'PERSONAL_INCOME', 'LOAN_NUM_TOTAL', 'LOAN_NUM_CLOSED'))

if compare_column in ['AGE', 'PERSONAL_INCOME']:
     fig, ax = plt.subplots()
     plt.hist(data.loc[data['TARGET'] == 0, compare_column], edgecolor = "black")
     plt.hist(data.loc[data['TARGET'] == 1, compare_column], edgecolor = "black")
     plt.legend([0, 1])
     st.pyplot(fig)
else:
     fig, ax = plt.subplots()
     plot_data = pd.crosstab(index = data[compare_column],
                             columns = data['TARGET'],
                             normalize = 'index')
     vals = list(map(str, list(plot_data.index)))
     dct_shares = plot_data.to_dict(orient='list')
     
     bottom = np.zeros(len(vals))
     for target, weight_count in dct_shares.items():
          p = ax.bar(vals, weight_count, label=target, bottom=bottom)
          bottom += weight_count

     st.pyplot(fig)
st.write('Доля откликов увеличивается при увеличении общего количества займов')
st.write('Уменьшается при увеличении числа детей и иждивенцев')
st.write('(для больших значений визуализация не информативна, так как мало данных)')
st.write('Доля откликов больше среди работающих людей')




st.divider()
st.write('**Числовые характеристики числовых столбцов**')
# Числовые характеристики числовых столбцов
num_column = st.selectbox(
     'Выберите показатель',
     ('TARGET', 'AGE', 'SOCSTATUS_WORK_FL',
       'SOCSTATUS_PENS_FL', 'GENDER', 'CHILD_TOTAL', 'DEPENDANTS',
       'PERSONAL_INCOME', 'LOAN_NUM_TOTAL', 'LOAN_NUM_CLOSED'))

stats_df = pd.DataFrame()
stats_df['median'] = [data[num_column].median()]
stats_df['mean'] = [data[num_column].mean()]
stats_df['std'] = [data[num_column].std()]
stats_df['min'] = [data[num_column].min()]
stats_df['25%'] = [data[num_column].quantile(0.25)]
stats_df['50%'] = [data[num_column].quantile(0.5)]
stats_df['75%'] = [data[num_column].quantile(0.75)]
stats_df['max'] = [data[num_column].max()]
st.table(stats_df)
st.write('Все показатели в норме, аномалии не наблюдаются')