import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

generated_link = "https://storage.yandexcloud.net/online/online.csv"
file = "~/Downloads/online.csv"

data = pd.read_csv(generated_link, names=["_", "utc", "value"])

df2 = data.iloc[[0, -1]]
print(df2)

data['utc'] = pd.to_datetime(data.utc, utc=True)
data['hm'] = (data.utc.dt.tz_convert('Europe/Moscow')).dt.floor('min').dt.time
data['hour'] = (data.utc.dt.tz_convert('Europe/Moscow')).dt.floor('min').dt.hour
data['day'] = (data.utc.dt.tz_convert('Europe/Moscow')).dt.day_name()

days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", 'Sunday']
data['day'] = pd.Categorical(data['day'], categories=days_order, ordered=True)

pivot_data = np.round(data.pivot_table(index='day', columns='hm', values='value', aggfunc='mean', sort=True))


plt.figure(figsize=(20, 10))
sns.heatmap(pivot_data, cmap=sns.color_palette("vlag", as_cmap=True), annot=True, fmt="g", square=False, linewidths=1,
            cbar_kws={'label': 'Средний онлайн'}, annot_kws={"fontsize": 6, 'rotation': 90})

plt.title("Средний онлайн по дням по часам")
plt.ylabel("День недели")
plt.xlabel("Час MSK")
plt.show()
