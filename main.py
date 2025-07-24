import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import shap
import plotly.express as px

data = np.load('shap_values.npz', allow_pickle=True)
df = pd.read_csv("dataset.csv")

shap_values = data['shap_values']
feature_names = data['feature_names'].tolist()
X_test = data['X_test']

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