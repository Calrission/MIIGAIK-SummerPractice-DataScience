import pickle
from sklearn.metrics import confusion_matrix
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import shap
import plotly.express as px
import plotly.graph_objects as go
data = np.load('shap_values.npz', allow_pickle=True)
df = pd.read_csv("dataset.csv")

with open('model.pkl', 'rb') as f:
    final_model = pickle.load(f)

shap_values = data['shap_values']
feature_names = data['feature_names'].tolist()
X_test = data['X_test']
y_test = data['y_test']

st.title("Струков Артемий Викторович_2023-ФГиИБ-ПИ-1б_21_Классификация_заёмщиков")
st.text("Данный дата-сет представляет упрощенную версию того, что могло быть в реальных данных, используемых для задач "
        "по анализу кредитоспособности населения. В реальных условиях, кол-во и глубина учитываемых параметров кратно "
        "больше того, что было представлено в дата-сете.")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Образцов", X_test.shape[0])
col2.metric("Признаков", X_test.shape[1])
col3.metric("Классов", shap_values.shape[2] if len(shap_values.shape) > 2 else 1)
col4.metric("Accuracy", "0.7800")
col5.metric("Weighted Recall", "0.7800")

class_idx = 0

plot_type = st.selectbox(
    "Тип визуализации",
    options=["dot", "bar"],
    index=0,
    help="dot: распределение влияния, bar: средняя важность"
)

max_display = st.slider(
    "Максимальное число признаков",
    min_value=5,
    max_value=min(50, len(feature_names)),
    value=12,
    help="Ограничьте число отображаемых признаков для лучшей читаемости"
)

st.subheader(f"SHAP Summary Plot (Класс {class_idx})")

fig, ax = plt.subplots(figsize=(10, 6))

shap.summary_plot(
    shap_values[:, :, class_idx],
    X_test,
    feature_names=feature_names,
    plot_type=plot_type,
    max_display=max_display,
    show=False
)

plt.title(f"Влияние признаков на класс {class_idx}", fontsize=14)
plt.tight_layout()

st.pyplot(fig)

status_class_percentage = pd.crosstab(
    index=df['checking_status'],
    columns=df['class'],
    normalize='index'
).reset_index()

melted_df = status_class_percentage.melt(
    id_vars='checking_status',
    var_name='class',
    value_name='percentage'
)

st.subheader("Распределение классов заемщиков по статусам расчетного счета")

fig = px.bar(
    melted_df,
    x='checking_status',
    y='percentage',
    color='class',
    color_discrete_sequence={0: '#ff5c5c', 1: '#a4c76f'},
    title='    ',
    labels={
        'checking_status': 'Статус',
        'percentage': 'Процентное соотношение (%)',
        'class': 'Класс заемщика'
    },
    text_auto='.1%',
    height=600
)

# Настройка внешнего вида
fig.update_layout(
    barmode='stack',
    xaxis_tickangle=-45,
    legend_title_text='Класс заемщика',
    legend_traceorder='reversed',
    hoverlabel=dict(bgcolor="black")
)

# Форматирование подписей
fig.update_traces(
    textposition='inside',
    textfont_color='black',
    textfont_size=12,
    textfont_family='Arial'
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Распределение классов заемщика по длительности кредита")

duration_bins = [0, 24, 60, float('inf')]
duration_labels = ['Короткие (<24)', 'Средние (25-60)', 'Длинные (>60)']
df['duration_group'] = pd.cut(df['duration'], bins=duration_bins, labels=duration_labels, right=False)

df['class_label'] = df['class'].map({1: 'Хороший', 0: 'Плохой', 'good': 'Хороший', 'bad': 'Плохой'})


cross_tab = pd.crosstab(
    index=df['duration_group'],
    columns=df['class_label'],
    normalize='index'
).reset_index()

melted_df = cross_tab.melt(
    id_vars='duration_group',
    var_name='class_label',
    value_name='proportion'
)

fig = px.bar(
    melted_df,
    x='duration_group',
    y='proportion',
    color='class_label',
    color_discrete_map={'Хороший': '#ff5c5c', 'Плохой': '#a4c76f'},
    barmode='group',
    text=[f'{val:.1%}' for val in melted_df['proportion']],
    title='       ',
    labels={
        'duration_group': 'Группа длительности кредита',
        'proportion': 'Доля заемщиков',
        'class_label': 'Класс заемщика'
    },
    height=500
)


fig.update_layout(
    xaxis_title='Группа длительности кредита',
    yaxis_title='Доля заемщиков',
    yaxis_tickformat='.0%',
    legend_title_text='Класс заемщика',
    hovermode='x unified',
    title_font_size=16,
    title_x=0.5
)

fig.update_traces(
    textposition='inside',
    textfont_size=12,
    textfont_color='black',
)

st.plotly_chart(fig, use_container_width=False)

y_test_pred = final_model.predict(X_test)
cm = confusion_matrix(y_test, y_test_pred)
classes = final_model.classes_

st.subheader("Интерактивная матрица ошибок")
classes = final_model.classes_

annotations = []
for i in range(len(classes)):
    for j in range(len(classes)):
        value = cm[i, j]
        percent = f"{value/cm.sum()*100:.1f}%" if cm.sum() > 0 else "0%"
        annotations.append(
            dict(
                x=j, y=i,
                text=f"<b>{value}</b><br>({percent})",
                showarrow=False,
                font=dict(color='white' if cm[i, j] > cm.max()/2 else 'black'),
                align="center"
            )
        )

# Создаем фигуру
fig = go.Figure(data=go.Heatmap(
    z=cm,
    x=classes,
    y=classes,
    colorscale='Blues',
    hoverongaps=False,
    hovertemplate="Истинный класс: %{y}<br>Предсказанный класс: %{x}<br>Количество: %{z}<extra></extra>",
    colorbar=dict(title="Количество"),
))

# Настраиваем оформление
fig.update_layout(
    title="   ",
    xaxis_title="Предсказанные классы",
    yaxis_title="Истинные классы",
    annotations=annotations,
    autosize=True,
    height=600,
    margin=dict(l=50, r=50, b=50, t=80),
    hoverlabel=dict(bgcolor="black", font_size=14),
    title_font=dict(size=20),
    font=dict(family="Arial"),
)

# Добавляем кнопки для переключения режимов
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            buttons=list([
                dict(
                    args=[{"z": [cm], "annotations": [annotations]}],
                    label="Абсолютные значения",
                    method="update"
                ),
                dict(
                    args=[{"z": [cm.astype('float')/cm.sum(axis=1)[:, np.newaxis]],
                          "annotations": []}],
                    label="Нормализованные",
                    method="update"
                )
            ]),
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.5,
            xanchor="center",
            y=1.15,
            yanchor="top"
        )
    ]
)

# Отображаем график
st.plotly_chart(fig, use_container_width=True)