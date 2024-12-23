import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# Giả định dữ liệu server log
data = {
    'Total_Requests': [1000, 1500, 1200, 2000, 2500],
    'HTTP_2xx': [900, 1400, 1100, 1900, 2400],
    'HTTP_4xx': [50, 50, 70, 60, 40],
    'HTTP_5xx': [50, 50, 30, 40, 60],
    'CPU_Usage': [60, 70, 65, 80, 90],
    'RAM_Usage': [70, 75, 72, 85, 88],
    'Error_Rate': [10, 6.67, 8.33, 5, 4]
}

# Chuyển dữ liệu thành DataFrame
df = pd.DataFrame(data)

# Xác định biến độc lập (X) và biến mục tiêu (y)
X = df[['Total_Requests', 'HTTP_2xx', 'HTTP_4xx', 'HTTP_5xx', 'CPU_Usage', 'RAM_Usage']]
y = df['Error_Rate']

# Chia dữ liệu thành tập huấn luyện và kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Sử dụng Random Forest Regression
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Dự đoán
y_pred = model.predict(X_test)

# Đánh giá mô hình
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error: {mae}")
print(f"R2 Score: {r2}")

# Dự báo phần trăm lỗi cho giá trị mới
new_data = [[3000, 2900, 50, 50, 85, 90]]  # Ví dụ dữ liệu mới
predicted_error_rate = model.predict(new_data)
print(f"Phần trăm lỗi dự báo: {predicted_error_rate[0]}%")
