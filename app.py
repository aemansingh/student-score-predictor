
import joblib
import pandas as pd
import streamlit as st

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Student Score Predictor",
    page_icon="🎓",
    layout="centered"
)

# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>
.block-container {
    max-width: 950px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

.home-hero {
    min-height: 62vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 1rem;
}

.home-badge {
    display: inline-block;
    padding: 10px 18px;
    margin-bottom: 28px;
    border: 1px solid #4569a8;
    border-radius: 30px;
    color: #91b7ff;
    font-size: 13px;
    letter-spacing: 1px;
}

.home-title {
    font-size: clamp(34px, 6vw, 58px);
    font-weight: 800;
    line-height: 1.2;
    letter-spacing: -1px;
    margin-bottom: 20px;
}

.home-subtitle {
    max-width: 580px;
    font-size: 18px;
    line-height: 1.8;
    opacity: 0.8;
}

.home-note {
    font-size: 14px;
    opacity: 0.6;
    margin-top: 18px;
}

.team-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    padding: 15px 10px;
    text-align: center;
    font-size: 13px;
    color: #999999;
    background: #0e1117;
    z-index: 100;
}

div[data-testid="stButton"] button,
div[data-testid="stFormSubmitButton"] button {
    min-height: 3rem;
    border-radius: 10px;
    font-weight: 600;
}

@media (max-width: 600px) {
    .home-hero {
        min-height: 55vh;
    }

    .team-footer {
        font-size: 10px;
    }
}
</style>
""", unsafe_allow_html=True)


# ---------------- LOAD MODEL ----------------

@st.cache_resource
def load_model():
    return joblib.load("student_score_model.joblib")


try:
    model = load_model()
except Exception as e:
    st.error(f"Could not load the prediction model: {e}")
    st.stop()


# ---------------- NAVIGATION ----------------

if "page" not in st.session_state:
    st.session_state.page = "home"


# =================================================
# HOME PAGE
# =================================================

if st.session_state.page == "home":

    # One continuous HTML fragment avoids Markdown
    # interpreting indented content as a code block.
    home_html = (
        '<div class="home-hero">'
        '<div class="home-badge">MACHINE LEARNING PROJECT</div>'
        '<div class="home-title">🎓 Student Score Predictor</div>'
        '<div class="home-subtitle">'
        'Discover your estimated academic performance through '
        'machine learning. Answer a few questions and get your '
        'predicted final score range.'
        '</div>'
        '<div class="home-note">'
        'Make better predictions. Understand your performance.'
        '</div>'
        '</div>'
    )

    st.markdown(home_html, unsafe_allow_html=True)

    _, center, _ = st.columns([1, 2, 1])

    with center:
        if st.button(
            "🚀 Start Prediction",
            type="primary",
            use_container_width=True
        ):
            st.session_state.page = "predict"
            st.rerun()

    footer_html = (
        '<div class="team-footer">'
        'By: Aeman Singh, Krishna Meena, Sayantika Roy, '
        'Reejul and Priya Chaudhary'
        '</div>'
    )

    st.markdown(footer_html, unsafe_allow_html=True)


# =================================================
# PREDICTION PAGE
# =================================================

elif st.session_state.page == "predict":

    left, right = st.columns([3, 1])

    with left:
        st.title("🎓 Student Score Predictor")

    with right:
        if st.button("← Home", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

    st.write(
        "Answer the following questions to estimate "
        "your final mathematics score."
    )

    st.divider()

    with st.form("student_form"):

        st.subheader("Academic Information")

        g1 = st.number_input(
            "1. What was your IST-1 score? (0–20)",
            min_value=0,
            max_value=20,
            value=10
        )

        g2 = st.number_input(
            "2. What was your IST-2 score? (0–20)",
            min_value=0,
            max_value=20,
            value=10
        )

        studytime = st.selectbox(
            "3. How many hours do you study per week?",
            [1, 2, 3, 4],
            format_func=lambda x: {
                1: "Less than 2 hours",
                2: "2–5 hours",
                3: "5–10 hours",
                4: "More than 10 hours"
            }[x]
        )

        failures = st.selectbox(
            "4. How many previous classes have you failed?",
            [0, 1, 2, 3],
            format_func=lambda x: "3 or more" if x == 3 else str(x)
        )

        absences = st.number_input(
            "5. How many school days have you missed?",
            min_value=0,
            max_value=75,
            value=0
        )

        st.divider()
        st.subheader("Study Environment")

        schoolsup = st.selectbox(
            "6. Do you receive extra educational support?",
            ["yes", "no"],
            format_func=lambda x: "Yes" if x == "yes" else "No"
        )

        famsup = st.selectbox(
            "7. Does your family support your studies?",
            ["yes", "no"],
            format_func=lambda x: "Yes" if x == "yes" else "No"
        )

        paid = st.selectbox(
            "8. Do you attend paid extra classes?",
            ["yes", "no"],
            format_func=lambda x: "Yes" if x == "yes" else "No"
        )

        freetime = st.select_slider(
            "9. How much free time do you have after school?",
            options=[1, 2, 3, 4, 5],
            value=3,
            format_func=lambda x: {
                1: "Very little",
                2: "A little",
                3: "Moderate",
                4: "Quite a lot",
                5: "A lot"
            }[x]
        )

        internet = st.selectbox(
            "10. Do you have internet access at home?",
            ["yes", "no"],
            format_func=lambda x: "Yes" if x == "yes" else "No"
        )

        submitted = st.form_submit_button(
            "🔮 Predict My Score",
            use_container_width=True,
            type="primary"
        )

    # ---------------- RESULTS ----------------

    if submitted:

        input_data = pd.DataFrame([{
            "G1": g1,
            "G2": g2,
            "studytime": studytime,
            "failures": failures,
            "absences": absences,
            "schoolsup": schoolsup,
            "famsup": famsup,
            "paid": paid,
            "freetime": freetime,
            "internet": internet
        }])

        predicted_grade = float(model.predict(input_data)[0])

        predicted_percentage = max(
            0.0,
            min(100.0, predicted_grade * 5)
        )

        lower = min(
            int(predicted_percentage // 5) * 5,
            95
        )
        upper = lower + 5

        st.divider()
        st.subheader("📊 Your Prediction")

        st.metric(
            "Estimated Final Score",
            f"{predicted_percentage:.1f}%"
        )

        st.success(
            f"Predicted Score Range: {lower}%–{upper}%"
        )

        st.progress(predicted_percentage / 100)

        st.caption(
            "This is an estimate, not a guarantee of actual marks."
        )

        with st.expander("About this prediction"):
            st.write(
                "The model uses Random Forest regression trained "
                "on 395 Portuguese secondary-school mathematics "
                "student records."
            )

            st.write(
                "Test-set mean absolute error: approximately "
                "1.16 grade points, or 5.8 percentage points."
            )

            st.write(
                "The model has not been validated on Indian "
                "college students. This project is intended "
                "for educational demonstration."
            )
