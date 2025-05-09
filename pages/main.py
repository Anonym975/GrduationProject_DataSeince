
import streamlit as st
import plotly.express as px
import pandas as pd
import streamlit_shadcn_ui as ui
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import yfinance as yf
from scipy.optimize import minimize

import time 
import warnings

from PIL import Image
# from Markuitz.interpretations import  optimization_strategies_info, appinfo ##metric_info, var_info,##
from portfolio_optimizer import PortfolioOptimizer


def main():
    st.markdown("""
    <style>
    @keyframes wave {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-10px); }
    }
    .wave-text {
        text-align: center;
        font-size: 34px;
        font-weight: bold;
        color: #0072ff;
        animation: wave 2s infinite;
    }
    </style>
    <div class="wave-text">📈 Smart Investing Starts Here</div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("### Input Parameters")
        with st.form("portfolio_form"):
            money = st.number_input(
                "💰 Enter how much you will invest ($)", 
                min_value=100.0, 
                step=100.0, 
                value=10000.0, 
                format="%.2f",
                help="Total capital you want to allocate"
            )

            UserReturn = st.number_input(
                "📊 Target Annual Return (%)",
                min_value=0.1,
                max_value=30.0,
                step=0.5,
                value=7.0,
                format="%.2f",
                help="Annual return you aim to achieve"
            )

            calculate = st.form_submit_button("🚀 Calculate")

    if calculate:
        with st.spinner("Buckle Up! Financial Wizardry in Progress...."):
            try:
                optimizer = PortfolioOptimizer(
                    ['AAPL', 'JNJ', 'PG', 'JPM', 'XOM', 'AMZN', 'KO', 'MSFT', 'GOLD', 'CVX'],
                    '2015-01-01',
                    '2023-12-30',
                    "stock_data.xlsx",
                    UserReturn,
                    0.044,
                )

                optimizer.optimized_allocation["allocation"] = optimizer.optimized_allocation["allocation"].apply(lambda x: round(x * 100, 2))
                optimizer.optimized_allocation.rename(columns={"allocation": "Allocation (%)"}, inplace=True)

            except Exception as e:
                st.error(f"An error occurred: {e}")
                return

        with st.container(border=True):
            main_tab1, main_tab2 = st.tabs(["Strategy: Minimum Risk", "Strategy: Target Return"])

            # ---- Minimum Risk ----
            with main_tab1:
                sub_tab1, sub_tab2 = st.tabs(["Summary", "Distribution"])
                with sub_tab1:
                    st.markdown("#### Optimization Portfolio with Minimum Risk")
                    w_opt_min = optimizer.singleEquationSolver()
                    risk_min = optimizer.riskFunction(w_opt_min)
                    return_min = optimizer.portfolioReturn(w_opt_min)

                    st.markdown(f"**Expected Annual Return**: {return_min:.2%}")
                    st.markdown(f"**Portfolio Risk**: {risk_min:.2%}")

                with sub_tab2:
                    allocations = optimizer.optimized_allocation.copy()
                    allocations["Tickers"] = allocations.index
                    st.table(allocations)

                    pie_data = allocations[allocations["Allocation (%)"] != 0]
                    fig = px.pie(pie_data, values="Allocation (%)", names="Tickers")
                    fig.update_layout(width=180, height=200, showlegend=False, margin=dict(t=20, b=0, l=0, r=0))
                    st.plotly_chart(fig, use_container_width=True)

            # ---- Target Return ----
            with main_tab2:
                sub_tab3, sub_tab4 = st.tabs(["Summary", "Distribution"])
                with sub_tab3:
                    st.markdown("#### Optimization Portfolio with Target Return")
                    daily_target_return = (1 + UserReturn / 100) ** (1/252) - 1
                    w_opt_target = optimizer.markowitz_optimal_weights_specific_return(daily_target_return)
                    risk_target = optimizer.riskFunction(w_opt_target)
                    return_target = optimizer.portfolioReturn(w_opt_target)

                    st.markdown(f"**Expected Annual Return**: {return_target:.2%}")
                    st.markdown(f"**Portfolio Risk**: {risk_target:.4%}")
                    st.markdown(f"**Sum of Weights**: {np.sum(w_opt_target):.4f}")

                    investment_required = np.sum(w_opt_target) * money
                    st.markdown(f"**To achieve your target return of {UserReturn:.2f}%, you need to invest:** ${investment_required:.2f}")
                    st.caption("Note: The sum of weights exceeds 1 because the optimizer adjusts allocations to meet your return target.")

                    # required_investment = np.sum(w_opt_target) * money
                    # st.markdown(f"💸 **Required Investment:** ${required_investment:.2f}")

                with sub_tab4:
                    allocations_target = optimizer.optimized_allocation.copy()
                    allocations_target["Tickers"] = allocations_target.index
                    st.table(allocations_target)

                    pie_data_target = allocations_target[allocations_target["Allocation (%)"] != 0]
                    fig = px.pie(pie_data_target, values="Allocation (%)", names="Tickers")
                    fig.update_layout(width=180, height=200, showlegend=False, margin=dict(t=20, b=0, l=0, r=0))
                    st.plotly_chart(fig, use_container_width=True)

    # Navigation Buttons
    time.sleep(1)
    col1, col2, col3 = st.columns([3, 4, 2])
    with col1:
        if st.button("⬅️ Back to Welcome"):
            st.switch_page("pages/wel.py")
    with col3:
        if st.button("➡️ Go to Performance"):
            st.switch_page("pages/performance.py")

main()


# def main():
#     ##تحميل الصورة وإعداد الصفحة
#     # im = Image.open("EfficientFrontier.png")
#     # st.set_page_config(page_title="Portfolio Optimization Dashboard", page_icon=im)
    
#     ##title in page
#     st.markdown("""
# <style>
# @keyframes wave {
#   0%, 100% { transform: translateY(0); }
#   50% { transform: translateY(-10px); }
# }

# .wave-text {
#     text-align: center;
#     font-size: 34px;
#     font-weight: bold;
#     color: #0072ff;
#     animation: wave 2s infinite;
# }
# </style>

# <div class="wave-text">📈 Smart Investing Starts Here</div>
# """, unsafe_allow_html=True)
   

    




#     cont1 = st.container(border=True)
#     cont1.markdown("### Input Parameters")
#     money = cont1.number_input(
#         "Enter How much you will invest ($)", value=None, step=100, placeholder="enter a number $..."##value=##default_tickers_str
#     )
   
    
        
#     UserReturn = cont1.number_input(
#         "Return of investment (%)",
#         min_value=0.0,
#         max_value=100.0,
#         step=5.0,
#         format="%0.8f",
#         value=None,
#         placeholder="enter persantage %...",
#         help = "enter return you want earn from your investment"
#     )
#     calc = cont1.button("Calculate")
#     if calc:
#         try:
#             with st.spinner("Buckle Up! Financial Wizardry in Progress...."):
#                 optimizer = PortfolioOptimizer(
#                     ['AAPL', 'JNJ', 'PG', 'JPM', 'XOM', 'AMZN', 'KO', 'MSFT', 'GOLD', 'CVX'],
#                     '2015-01-01',
#                     '2023-12-30',
#                     "stock_data.xlsx",
#                     UserReturn,
#                     0.044,
#                 )
#                 # Get and process optimized allocation (as DataFrame)
#                 optimizer.optimized_allocation["allocation"] = optimizer.optimized_allocation["allocation"].apply(lambda x: round(x * 100, 2))

#                 # Rename for clarity in display
#                 optimizer.optimized_allocation.rename(columns={"allocation": "Allocation (%)"}, inplace=True)

#         except ValueError as e:
#             st.error("Unable to download data for one or more tickers!")
#             return
#         except Exception as e:
#             st.error(str(e))
#             return 
               
#         with st.container(border=True):
#             main_tab1, main_tab2 = st.tabs(["Strategy: Minimum Risk", "Strategy: Target Return"])

#             # Strategy 1: Minimum Risk
#             with main_tab1:
#                 sub_tab1, sub_tab2 = st.tabs(["Summary", "Distribution"])

#                 with sub_tab1:
#                     st.markdown("#### Optimization Portfolio with Minimum Risk")
#                     w_opt_markowitz = optimizer.singleEquationSolver()
#                     risk_markowitz = optimizer.riskFunction(w_opt_markowitz)
#                     ret_markowitz = optimizer.portfolioReturn(w_opt_markowitz)

#                     st.markdown(f"**Expected Annual Return**: {ret_markowitz:.2%}")
#                     st.markdown(f"**Portfolio Risk**: {risk_markowitz:.2%}")

#                 with sub_tab2:
#                     st.markdown("#### Optimized Portfolio Distribution (Minimum Risk)")
#                     allocations_min_risk = optimizer.optimized_allocation.copy()
#                     allocations_min_risk["Tickers"] = allocations_min_risk.index
#                     allocations_min_risk = allocations_min_risk[["Tickers", "Allocation (%)"]]
#                     st.table(allocations_min_risk)

#                     pie_data = allocations_min_risk[allocations_min_risk["Allocation (%)"] != 0]
#                     fig = px.pie(pie_data, values="Allocation (%)", names=pie_data["Tickers"])
#                     fig.update_layout(width=180, height=200, showlegend=False, margin=dict(t=20, b=0, l=0, r=0))
#                     st.plotly_chart(fig, use_container_width=True)

#             # Strategy 2: Target Return
#             with main_tab2:
#                 sub_tab3, sub_tab4 = st.tabs(["Summary", "Distribution"])  # ملاحظة تغيير الاسم

#                 with sub_tab3:
#                     st.markdown("#### Optimization Portfolio with Target Return")
#                     w_opt_specific_return = optimizer.markowitz_optimal_weights_specific_return(UserReturn / 100)
#                     risk_specific_return = optimizer.riskFunction(w_opt_specific_return)
#                     ret_specific_return = optimizer.portfolioReturn(w_opt_specific_return)

#                     st.markdown(f"**Expected Annual Return**: {ret_specific_return:.2%}")
#                     st.markdown(f"**Portfolio Risk**: {risk_specific_return:.4%}")
#                     st.markdown(f"Sum of Weights: {np.sum(w_opt_specific_return):.4f}")

#                     investment_required = np.sum(w_opt_specific_return) * money
#                     st.markdown(f"**To achieve your target return of {UserReturn:.2f}%, you need to invest:** ${investment_required:.2f}")
#                     st.caption("Note: The sum of weights exceeds 1 because the optimizer adjusts allocations to meet your return target.")

#                 with sub_tab4:
#                     st.markdown("#### Optimized Portfolio Distribution (Target Return)")
#                     allocations_target = optimizer.optimized_allocation.copy()
#                     allocations_target["Tickers"] = allocations_target.index
#                     allocations_target = allocations_target[["Tickers", "Allocation (%)"]]
#                     st.table(allocations_target)

#                     pie_data_target = allocations_target[allocations_target["Allocation (%)"] != 0]
#                     fig = px.pie(pie_data_target, values="Allocation (%)", names=pie_data_target["Tickers"])
#                     fig.update_layout(width=180, height=200, showlegend=False, margin=dict(t=20, b=0, l=0, r=0))
#                     st.plotly_chart(fig, use_container_width=True)






#     # تأثير عند الانتقال بين الصفحات
#     with st.spinner('Loading...'):
#         time.sleep(1)  # الانتظار قبل الانتقال
                                 
#     col1, col2, col3 = st.columns([3, 4, 2])

#     with col1:
#         if st.button("⬅️ Back to Welcome"):
#             st.switch_page("pages/wel.py")
#             st.experimental_rerun()

#     with col3:
#         if st.button("➡️ Go to Performance"):
#             st.switch_page("pages/performance.py")
#             st.experimental_rerun()

# # if __name__ == "__main__":
# main()

