import streamlit as st
import matplotlib.pyplot as plt

# CSS để tùy chỉnh màu sắc và responsive
st.markdown("""
    <style>
    /* Tùy chỉnh ô nhập liệu */
    .stNumberInput > div > input {
        width: 100%;
        padding: 8px;
        border: 2px solid #4CAF50; /* Viền xanh lá */
        border-radius: 5px;
        background-color: #F5F7F5; /* Nền xám nhạt */
        color: #333; /* Chữ xám đậm */
        font-size: 16px;
    }
    .stSelectbox > div > select {
        width: 100%;
        padding: 8px;
        border: 2px solid #FF9800; /* Viền cam */
        border-radius: 5px;
        background-color: #FFF3E0; /* Nền cam nhạt */
        color: #333;
        font-size: 16px;
    }
    /* Tùy chỉnh nút bấm */
    .stButton > button {
        width: 100%;
        padding: 10px;
        background-color: #4CAF50; /* Nền xanh lá */
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 16px;
        font-weight: bold;
        transition: background-color 0.3s;
    }
    .stButton > button:hover {
        background-color: #45A049; /* Xanh đậm hơn khi hover */
    }
    /* Responsive */
    @media (max-width: 600px) {
        .stColumn {
            width: 100% !important;
            margin-bottom: 10px;
        }
        .stButton > button {
            width: 100%;
        }
    }
    @media (min-width: 601px) and (max-width: 900px) {
        .stColumn {
            width: 50% !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Từ điển dịch ngôn ngữ
translations = {
    "vi": {
        "title": "Tính Chỉ Số BMI Theo Độ Tuổi",
        "age_label": "Tuổi (0-100):",
        "gender_label": "Giới tính:",
        "male": "Nam",
        "female": "Nữ",
        "weight_label": "Cân nặng (kg):",
        "height_label": "Chiều cao (cm):",
        "calculate_button": "Tính BMI",
        "bmi_result": "Chỉ số BMI của bạn là: **{bmi:.2f}**",
        "category_label": "Phân loại (tuổi {age}, {gender}): **{category}**",
        "adult_category_label": "Phân loại (18+): **{category}**",
        "advice_label": "Lời khuyên ngộ nghĩnh: {advice}",
        "child_note": "Lưu ý: Kết quả dựa trên biểu đồ percentile. Hãy hỏi bác sĩ để biết thêm nha!",
        "height_error": "Chiều cao phải lớn hơn 0 nha!",
        "chart_title": "Biểu đồ BMI siêu xịn",
        "no_data": "Ôi, chưa có dữ liệu percentile cho tuổi này đâu!"
    },
    "en": {
        "title": "Calculate BMI by Age",
        "age_label": "Age (0-100):",
        "gender_label": "Gender:",
        "male": "Male",
        "female": "Female",
        "weight_label": "Weight (kg):",
        "height_label": "Height (cm):",
        "calculate_button": "Calculate BMI",
        "bmi_result": "Your BMI is: **{bmi:.2f}**",
        "category_label": "Classification (age {age}, {gender}): **{category}**",
        "adult_category_label": "Classification (18+): **{category}**",
        "advice_label": "Fun advice: {advice}",
        "child_note": "Note: Results are based on percentile charts. Ask a doctor for more details!",
        "height_error": "Height must be greater than 0, buddy!",
        "chart_title": "Super Cool BMI Chart",
        "no_data": "Oops, no percentile data for this age yet!"
    }
}

# Dữ liệu percentile (giả lập WHO/CDC cho trẻ em 2-17 tuổi)
percentile_data = {
    "male": {
        2: {"P5": 12.5, "P50": 14.5, "P85": 16.5, "P95": 17.5},
        3: {"P5": 12.7, "P50": 14.7, "P85": 16.7, "P95": 17.8},
        4: {"P5": 12.9, "P50": 14.9, "P85": 16.9, "P95": 18.0},
        5: {"P5": 13.0, "P50": 15.0, "P85": 17.0, "P95": 18.5},
        6: {"P5": 13.2, "P50": 15.3, "P85": 17.5, "P95": 19.0},
        7: {"P5": 13.5, "P50": 15.7, "P85": 18.0, "P95": 19.7},
        8: {"P5": 13.8, "P50": 16.2, "P85": 18.7, "P95": 20.5},
        9: {"P5": 14.0, "P50": 16.7, "P85": 19.5, "P95": 21.5},
        10: {"P5": 14.3, "P50": 17.3, "P85": 20.3, "P95": 22.5},
        11: {"P5": 14.7, "P50": 18.0, "P85": 21.2, "P95": 23.5},
        12: {"P5": 15.1, "P50": 18.7, "P85": 22.2, "P95": 24.5},
        13: {"P5": 15.6, "P50": 19.5, "P85": 23.2, "P95": 25.5},
        14: {"P5": 16.2, "P50": 20.3, "P85": 24.2, "P95": 26.5},
        15: {"P5": 16.8, "P50": 21.1, "P85": 25.1, "P95": 27.5},
        16: {"P5": 17.3, "P50": 21.8, "P85": 25.9, "P95": 28.3},
        17: {"P5": 17.8, "P50": 22.4, "P85": 26.5, "P95": 29.0}
    },
    "female": {
        2: {"P5": 12.3, "P50": 14.3, "P85": 16.3, "P95": 17.3},
        3: {"P5": 12.5, "P50": 14.5, "P85": 16.5, "P95": 17.6},
        4: {"P5": 12.7, "P50": 14.7, "P85": 16.8, "P95": 17.9},
        5: {"P5": 12.8, "P50": 14.8, "P85": 17.0, "P95": 18.2},
        6: {"P5": 13.0, "P50": 15.0, "P85": 17.4, "P95": 18.7},
        7: {"P5": 13.3, "P50": 15.4, "P85": 18.0, "P95": 19.4},
        8: {"P5": 13.6, "P50": 15.9, "P85": 18.7, "P95": 20.3},
        9: {"P5": 14.0, "P50": 16.5, "P85": 19.6, "P95": 21.4},
        10: {"P5": 14.4, "P50": 17.2, "P85": 20.6, "P95": 22.6},
        11: {"P5": 14.9, "P50": 18.0, "P85": 21.7, "P95": 23.9},
        12: {"P5": 15.5, "P50": 18.9, "P85": 22.9, "P95": 25.2},
        13: {"P5": 16.1, "P50": 19.8, "P85": 24.0, "P95": 26.4},
        14: {"P5": 16.7, "P50": 20.6, "P85": 24.9, "P95": 27.4},
        15: {"P5": 17.2, "P50": 21.3, "P85": 25.7, "P95": 28.2},
        16: {"P5": 17.6, "P50": 21.9, "P85": 26.3, "P95": 28.9},
        17: {"P5": 17.9, "P50": 22.3, "P85": 26.8, "P95": 29.5}
    }
}

# Hàm tính BMI
def calculate_bmi(weight, height_m):
    return weight / (height_m * height_m)

# Hàm phân loại BMI cho trẻ em
def classify_bmi_children(bmi, age, gender, lang):
    available_ages = sorted(percentile_data[gender].keys())
    closest_age = min(available_ages, key=lambda x: abs(x - age))
    
    if closest_age not in percentile_data[gender]:
        return "Không có dữ liệu", translations[lang]["no_data"]
    
    percentiles = percentile_data[gender][closest_age]
    if bmi < percentiles["P5"]:
        return "Gầy (dưới P5)", "Hãy làm bạn với rau xanh và sữa, chúng đang chờ để giúp bạn khỏe hơn đấy! 😺"
    elif percentiles["P5"] <= bmi < percentiles["P85"]:
        return "Bình thường (P5-P85)", "Tuyệt vời! Cứ nhảy nhót, chạy chơi và ăn đủ chất để giữ dáng siêu xịn nha! 🐶"
    elif percentiles["P85"] <= bmi < percentiles["P95"]:
        return "Thừa cân (P85-P95)", "Ôi, bớt ăn bánh ngọt tí nha, cùng chạy bộ với chú cún để dáng đẹp hơn nào! 🐾"
    else:
        return "Béo phì (trên P95)", "Đừng lo, hãy làm siêu anh hùng: ăn rau, tập thể thao, bác sĩ sẽ giúp bạn chiến thắng! 💪"

# Hàm phân loại BMI cho người lớn
def classify_bmi_adult(bmi, lang):
    if bmi < 18.5:
        return "Gầy", "Hãy mời cơ thể bạn một bữa tiệc protein và trái cây, nó sẽ cảm ơn bạn bằng năng lượng dồi dào! 🍎"
    elif 18.5 <= bmi <= 24.9:
        return "Bình thường", "Bạn là ngôi sao cân đối! Cứ giữ vibe tích cực, gym nhẹ và salad vui vẻ nha! 🌟"
    elif 25 <= bmi <= 29.9:
        return "Thừa cân", "Tí tẹo năng lượng dư thôi! Đi bộ với bạn thân, bỏ bớt snack đêm khuya, dáng sẽ xinh ngay! 🚶"
    else:
        return "Béo phì", "Bắt đầu hành trình siêu nhân nào: nhảy dây, ăn rau, bác sĩ sẽ là đồng đội giúp bạn tỏa sáng! 🦸"

# Hàm vẽ biểu đồ (dạng vùng)
def plot_bmi_chart(bmi, age, gender, lang):
    fig, ax = plt.subplots(figsize=(8, 4))
    
    if age <= 17:
        available_ages = sorted(percentile_data[gender].keys())
        closest_age = min(available_ages, key=lambda x: abs(x - age))
        percentiles = percentile_data[gender][closest_age]
        categories = ["Gầy (<P5)", "Bình thường (P5-P85)", "Thừa cân (P85-P95)", "Béo phì (>P95)"]
        thresholds = [0, percentiles["P5"], percentiles["P85"], percentiles["P95"], percentiles["P95"] + 10]
        colors = ['#FF9999', '#66CC99', '#FFCC99', '#FF6666']
        for i in range(len(thresholds)-1):
            ax.fill_betweenx([0, 1], thresholds[i], thresholds[i+1], color=colors[i], alpha=0.5, label=categories[i])
        ax.axvline(x=bmi, color='red', linestyle='--', label=f"BMI: {bmi:.2f}")
        ax.set_xlim(0, thresholds[-1])
        ax.set_ylim(0, 1)
        ax.set_yticks([])
    else:
        categories = ["Gầy", "Bình thường", "Thừa cân", "Béo phì"]
        thresholds = [0, 18.5, 24.9, 29.9, 40]
        colors = ['#FF9999', '#66CC99', '#FFCC99', '#FF6666']
        for i in range(len(thresholds)-1):
            ax.fill_betweenx([0, 1], thresholds[i], thresholds[i+1], color=colors[i], alpha=0.5, label=categories[i])
        ax.axvline(x=bmi, color='red', linestyle='--', label=f"BMI: {bmi:.2f}")
        ax.set_xlim(0, 40)
        ax.set_ylim(0, 1)
        ax.set_yticks([])
    
    ax.set_xlabel("BMI")
    ax.set_title(translations[lang]["chart_title"])
    ax.legend(loc='upper left')
    st.pyplot(fig)

# Giao diện Streamlit
st.title(translations["vi"]["title"])

# Chọn ngôn ngữ
language = st.selectbox("Ngôn ngữ / Language:", ["Tiếng Việt", "English"], index=0)
lang = "vi" if language == "Tiếng Việt" else "en"

# Khung nhập liệu responsive với màu sắc
st.subheader("Nhập thông tin của bạn")
col1, col2 = st.columns(2)
with col1:
    col_age, col_gender = st.columns(2)
    with col_age:
        age = st.number_input(translations[lang]["age_label"], min_value=0, max_value=100, step=1, key="age")
    with col_gender:
        gender = st.selectbox(translations[lang]["gender_label"], [translations[lang]["male"], translations[lang]["female"]], key="gender")
        gender_key = "male" if gender == translations[lang]["male"] else "female"
with col2:
    col_weight, col_height = st.columns(2)
    with col_weight:
        weight = st.number_input(translations[lang]["weight_label"], min_value=1.0, max_value=300.0, step=0.1, key="weight")
    with col_height:
        height_cm = st.number_input(translations[lang]["height_label"], min_value=30.0, max_value=300.0, step=0.1, key="height")

# Chuyển đổi chiều cao từ cm sang m
height_m = height_cm / 100

# Nút tính toán
if st.button(translations[lang]["calculate_button"]):
    if height_m > 0:
        bmi = calculate_bmi(weight, height_m)
        st.write(f"Chiều cao: {height_cm} cm = {height_m:.2f} m")
        st.write(translations[lang]["bmi_result"].format(bmi=bmi))

        # Phân loại và lời khuyên
        if age <= 17:
            category, advice = classify_bmi_children(bmi, age, gender_key, lang)
            if category == "Không có dữ liệu":
                st.warning(translations[lang]["no_data"])
            else:
                st.write(translations[lang]["category_label"].format(age=age, gender=gender, category=category))
                st.write(translations[lang]["advice_label"].format(advice=advice))
                st.write(translations[lang]["child_note"])
        else:
            category, advice = classify_bmi_adult(bmi, lang)
            st.write(translations[lang]["adult_category_label"].format(category=category))
            st.write(translations[lang]["advice_label"].format(advice=advice))

        # Vẽ biểu đồ
        st.write(f"### {translations[lang]['chart_title']}")
        plot_bmi_chart(bmi, age, gender_key, lang)
    else:
        st.error(translations[lang]["height_error"])

st.write("---")
st.write("Ứng dụng này cung cấp kết quả tham khảo. Hãy hỏi bác sĩ để biết thêm nha!" if lang == "vi" else "This app provides reference results. Ask a doctor for more details!")
