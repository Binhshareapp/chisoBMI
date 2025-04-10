import streamlit as st
import matplotlib.pyplot as plt

# Hàm tính BMI
def calculate_bmi(weight, height_m):
    return weight / (height_m * height_m)

# Hàm phân loại BMI cho trẻ em (0-17 tuổi)
def classify_bmi_children(bmi, age):
    if age <= 5:
        if bmi < 14: return "Gầy", "Tăng cường dinh dưỡng, tham khảo bác sĩ nhi khoa."
        elif 14 <= bmi <= 18: return "Bình thường", "Duy trì chế độ ăn uống và vận động hợp lý."
        else: return "Thừa cân/Béo phì", "Kiểm soát cân nặng, giảm đồ ăn nhanh, tăng vận động."
    elif 6 <= age <= 12:
        if bmi < 15: return "Gầy", "Bổ sung dinh dưỡng, theo dõi sức khỏe định kỳ."
        elif 15 <= bmi <= 20: return "Bình thường", "Tiếp tục duy trì lối sống lành mạnh."
        else: return "Thừa cân/Béo phì", "Hạn chế đồ ngọt, tập thể dục đều đặn."
    else:  # 13-17 tuổi
        if bmi < 17: return "Gầy", "Ăn uống đủ chất, kiểm tra sức khỏe nếu cần."
        elif 17 <= bmi <= 23: return "Bình thường", "Giữ thói quen tốt, vận động thường xuyên."
        else: return "Thừa cân/Béo phì", "Giảm cân từ từ, tham khảo chuyên gia dinh dưỡng."

# Hàm phân loại BMI cho người lớn (18+)
def classify_bmi_adult(bmi):
    if bmi < 18.5: return "Gầy", "Tăng cân bằng chế độ ăn giàu dinh dưỡng, tập luyện nhẹ."
    elif 18.5 <= bmi <= 24.9: return "Bình thường", "Duy trì lối sống lành mạnh, kiểm tra sức khỏe định kỳ."
    elif 25 <= bmi <= 29.9: return "Thừa cân", "Giảm cân nhẹ, tăng cường vận động, ăn uống cân bằng."
    else: return "Béo phì", "Tham khảo bác sĩ để giảm cân an toàn, tránh bệnh liên quan."

# Hàm vẽ biểu đồ
def plot_bmi_chart(bmi, age):
    fig, ax = plt.subplots()
    if age <= 17:
        if age <= 5:
            categories = ["Gầy", "Bình thường", "Thừa cân/Béo phì"]
            thresholds = [0, 14, 18, 25]
        elif 6 <= age <= 12:
            categories = ["Gầy", "Bình thường", "Thừa cân/Béo phì"]
            thresholds = [0, 15, 20, 25]
        else:  # 13-17
            categories = ["Gầy", "Bình thường", "Thừa cân/Béo phì"]
            thresholds = [0, 17, 23, 30]
    else:
        categories = ["Gầy", "Bình thường", "Thừa cân", "Béo phì"]
        thresholds = [0, 18.5, 24.9, 29.9, 40]

    heights = [thresholds[i+1] - thresholds[i] for i in range(len(thresholds)-1)]
    ax.bar(categories, heights, color=['#FF9999', '#66CC99', '#FFCC99', '#FF6666'][:len(categories)])
    ax.axhline(y=bmi, color='red', linestyle='--', label=f"BMI của bạn: {bmi:.2f}")
    ax.set_ylabel("BMI")
    ax.set_title("So sánh BMI của bạn")
    ax.legend()
    st.pyplot(fig)

# Giao diện Streamlit
st.title("Tính Chỉ Số BMI Theo Độ Tuổi")

# Nhập thông tin từ người dùng với kiểm tra cơ bản
try:
    age = st.number_input("Nhập tuổi (0-100):", min_value=0, max_value=100, step=1)
    weight = st.number_input("Nhập cân nặng (kg):", min_value=1.0, max_value=300.0, step=0.1)
    height_cm = st.number_input("Nhập chiều cao (cm):", min_value=30.0, max_value=300.0, step=0.1)

    if age < 0 or weight <= 0 or height_cm <= 0:
        raise ValueError("Tuổi, cân nặng và chiều cao phải lớn hơn 0!")

    # Chuyển đổi chiều cao từ cm sang m
    height_m = height_cm / 100

    # Nút tính toán
    if st.button("Tính BMI"):
        bmi = calculate_bmi(weight, height_m)
        st.write(f"Chiều cao: {height_cm} cm = {height_m:.2f} m")
        st.success(f"Chỉ số BMI của bạn là: **{bmi:.2f}**")

        # Phân loại và lời khuyên
        if age <= 17:
            category, advice = classify_bmi_children(bmi, age)
            st.write(f"Phân loại (tuổi {age}): **{category}**")
            st.write(f"Lời khuyên: {advice}")
            st.info("Lưu ý: Với trẻ em, kết quả chính xác cần tham khảo biểu đồ percentile từ bác sĩ.")
        else:
            category, advice = classify_bmi_adult(bmi)
            st.write(f"Phân loại (18+): **{category}**")
            st.write(f"Lời khuyên: {advice}")

        # Vẽ biểu đồ
        st.write("### Biểu đồ trực quan")
        plot_bmi_chart(bmi, age)

except ValueError as e:
    st.error(f"Lỗi: {e}")

st.write("---")
st.write("Ứng dụng này cung cấp kết quả tham khảo. Hãy tham khảo ý kiến bác sĩ để đánh giá chính xác.")
