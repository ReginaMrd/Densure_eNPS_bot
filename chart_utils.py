# chart_utils.py

import matplotlib.pyplot as plt

def build_pie_chart(promoters, passives, detractors):
    labels = ['Promoters', 'Passives', 'Detractors']
    sizes = [promoters, passives, detractors]
    colors = ['lightgreen', 'lightblue', 'lightcoral']
    explode = (0.1, 0.1, 0.1)  # выделим промоутеров

    plt.figure(figsize=(7, 7))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')  # равные пропорции для круга
    plt.title('Distribution of Responses')
    plt.savefig('pie_chart.png')  # сохраняем диаграмму в файл
