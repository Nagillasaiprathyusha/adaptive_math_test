import streamlit as st
import time
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from ai_model import generate_ai_question
from ml_model import predict_difficulty
from performance import evaluate_performance, plot_time_chart

def main():
    st.title("Adaptive Math Test")

    num_questions = 15  # Set the total number of questions

    if 'test_started' not in st.session_state:
        st.session_state['test_started'] = False
        st.session_state['current_question_index'] = 0
        st.session_state['score'] = 0
        st.session_state['time_taken'] = []
        st.session_state['question_log'] = []
        st.session_state['difficulty'] = 1  # Start at difficulty 1
        st.session_state['total_questions'] = num_questions
        st.session_state['correct_answer'] = None  # To store the actual answer

    if not st.session_state['test_started']:
        if st.button("Start Test"):
            st.session_state['test_started'] = True
            st.session_state['start_time'] = time.time()
            question_data = generate_ai_question(st.session_state['difficulty'])
            if question_data and 'question' in question_data and 'answer' in question_data:
                st.session_state['current_question_data'] = question_data
                st.session_state['correct_answer'] = question_data['answer']
                st.session_state['user_answer'] = ""
                st.rerun()
            else:
                st.error("Failed to generate the first question with necessary data.")
    else:
        if st.session_state['current_question_index'] < st.session_state['total_questions']:
            question_data = st.session_state['current_question_data']
            st.subheader(f"Question {st.session_state['current_question_index'] + 1}: [Difficulty: {st.session_state['difficulty']}] {question_data['question']}")
            user_answer = st.text_input("Your Answer:", key=f"answer_{st.session_state['current_question_index']}", value=st.session_state.get('user_answer', ""))

            if st.button("Submit"):
                if user_answer:
                    end_time = time.time()
                    duration = round(end_time - st.session_state['start_time'], 2)
                    st.session_state['time_taken'].append(duration)

                    is_correct = False
                    try:
                        if st.session_state['correct_answer'] is not None and float(user_answer.strip()) == float(st.session_state['correct_answer']):
                            st.success("Correct!")
                            correct = 1
                            st.session_state['score'] += 1
                            is_correct = True
                        else:
                            st.error(f"Incorrect! The correct answer was {st.session_state['correct_answer']}")
                            correct = 0
                    except ValueError:
                        st.error("Invalid input. Please enter a number.")
                        correct = 0

                    st.session_state['question_log'].append({
                        "question": question_data["question"],
                        "user_answer": user_answer,
                        "correct_answer": st.session_state['correct_answer'],
                        "correct": "Yes" if correct else "No",
                        "time": duration,
                        "difficulty": question_data['difficulty_level']
                    })

                    st.session_state['difficulty'] = predict_difficulty(is_correct, duration, st.session_state['difficulty'])
                    st.session_state['current_question_index'] += 1
                    st.session_state['user_answer'] = ""
                    st.session_state['correct_answer'] = None # Reset correct answer

                    if st.session_state['current_question_index'] < st.session_state['total_questions']:
                        next_question_data = generate_ai_question(st.session_state['difficulty'])
                        if next_question_data and 'question' in next_question_data and 'answer' in next_question_data:
                            st.session_state['current_question_data'] = next_question_data
                            st.session_state['correct_answer'] = next_question_data['answer']
                            st.rerun()
                        else:
                            st.error("Failed to generate the next question with necessary data.")
                    else:
                        st.rerun()
                else:
                    st.warning("Please enter your answer.")

        else:
            st.subheader("Test Finished!")
            st.write(f"Final Score: {st.session_state['score']}/{st.session_state['total_questions']}") # Display scoreboard
            evaluate_performance(st.session_state['score'], st.session_state['total_questions'], st.session_state['time_taken'])
            plot_time_chart(st.session_state['time_taken'])
            if st.button("Restart Test"):
                for key in st.session_state.keys():
                    del st.session_state[key]
                st.rerun()

if __name__ == "__main__":
    main()
