import matplotlib.pyplot as plt
import streamlit as st

def evaluate_performance(score, total, times):
    avg_time = sum(times) / len(times) if times else 0
    st.write("\n--- Test Summary ---")
    st.write(f"Score: {score}/{total}")
    st.write(f"Average Time: {avg_time:.2f} seconds")

    if score >= 0.8 * total:
        st.write("Excellent performance!")
    elif score >= 0.6 * total:
        st.write("Good job, keep improving.")
    else:
        st.write("Needs more practice.")

def plot_time_chart(times):
    if times:
        fig, ax = plt.subplots()
        ax.plot(range(1, len(times) + 1), times, marker='o', color='blue')
        ax.set_title("Time Taken per Question")
        ax.set_xlabel("Question Number")
        ax.set_ylabel("Time (seconds)")
        ax.grid(True)
        st.pyplot(fig)
