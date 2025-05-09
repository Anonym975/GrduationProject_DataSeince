import streamlit as st
import time

col1, col2 = st.columns([0.14, 0.86], gap="small")
col1.write("`Website Created by:`")
linkedin_url = "http://www.linkedin.com/in/khaledomarmohammed/"
col2.markdown(
        f'<a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="15" height="15" style="vertical-align: middle; margin-right: 10px;">Khaled Omar</a>',
        unsafe_allow_html=True,
    )

col1, col2 = st.columns([0.14, 0.86], gap="small")
col1.write("`Team Leader and Statical Model Created by:`")
linkedin_url_omar = "https://www.linkedin.com/in/omar-mohamed-b8813123b/"  # الرابط الجديد لعمر محمد
col2.markdown(
        f'<a href="{linkedin_url_omar}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="15" height="15" style="vertical-align: middle; margin-right: 10px;">Omar Mohammed</a>',
        unsafe_allow_html=True,
    )




st.markdown("""
## 📝 Project Overview

This project implements **Markowitz Portfolio Theory** by applying **mean-variance optimization** to help users achieve the highest possible return while minimizing risk.  
We employ **Markowitz** and **Target Return** strategies to ensure optimized asset allocation with the lowest risk levels achievable through these strategies. 

---

## 🛠 Key Features

- **Optimal Portfolio Weights**: Using historical data, the app calculates the best asset allocation that minimizes the portfolio's risk for a given return.

- **Risk-Return Tradeoff**: The tool helps you understand the balance between risk and return, offering insights into efficient frontiers and the capital market line.

- 🎯 **Target Return Strategy**: Allows investors to set a target return, and the app calculates the necessary portfolio weights and amount to achieve it with the minimum risk.

- 📊 **Markowitz Strategy**: Focuses on creating the minimum-risk portfolio given expected returns and variances of assets.

---

## 💡 Why Markowitz?

The Markowitz Model revolutionized investment management by introducing the concept of diversification.  
It shows that investors can reduce risk by carefully selecting a mix of assets, even if those assets have different returns, correlations, and volatilities.

---
## 👥 Development Team

- **Khaled Omar**  
- **Omar Mohammed** (Team Leader)  
- **Mohammed Osama**  
- **Esraa Harby**  
- **Alaa Ashraf**  

---

## 📚 Tools & Resources

- **Python Libraries**: Streamlit, NumPy, Pandas, Plotly.Express, Yfinance, Scipy.Pptimize  
- **Finance Concepts**: Modern Portfolio Theory, Risk vs. Return, Markowitz, Target Return

---

## 💡 Goal

To provide a practical tool for portfolio optimization based on financial theory and real data visualization.  
We aim to help investors understand the optimal allocation of assets with the least risk achievable through the mentioned strategies.

---

## 🛠 Key Features

- **Optimal Portfolio Weights**: Using historical data, the app calculates the best asset allocation that minimizes the portfolio's risk for a given return.

- **Risk-Return Tradeoff**: The tool helps you understand the balance between risk and return, offering insights into efficient frontiers and the capital market line.

- 🎯 **Target Return Strategy**: Allows investors to set a target return, and the app calculates the necessary portfolio weights and amount to achieve it with the minimum risk.

- 📊 **Markowitz Strategy**: Focuses on creating the minimum-risk portfolio given expected returns and variances of assets.

---

## 💡 Why Markowitz?

The Markowitz Model revolutionized investment management by introducing the concept of diversification.  
It shows that investors can reduce risk by carefully selecting a mix of assets, even if those assets have different returns, correlations, and volatilities.

---

🎓 **Final Year Project**
This project is a graduation project that combines academic knowledge in finance with practical software development skills, aimed at providing an efficient solution for real-world investment portfolio management.


""")


# Effect when switching between pages
with st.spinner('Loading...'):
    time.sleep(1)  # Wait before switching

col1, col2, col3 = st.columns([3, 6, 3])

# Back to Welcome Page
with col1:
    if st.button("⬅️ Back to Welcome"):
        st.switch_page("pages/wel.py")
        st.experimental_rerun()

# Go to Portfolio Page
with col3:
    if st.button("➡️ Go to Portfolio"):
        st.switch_page("pages/main.py")
        st.experimental_rerun()
