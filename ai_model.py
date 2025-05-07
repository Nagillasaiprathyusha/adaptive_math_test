from transformers import pipeline
import streamlit as st
import random

try:
    question_generator = pipeline("text-generation", model="gpt2")
except Exception as e:
    print(f"Error loading the AI model: {e}")
    question_generator = None
    st.error(f"Error loading the AI model: {e}")

def generate_ai_question(difficulty):
    if question_generator is None:
        return {"question": "Error loading AI model.", "answer": "N/A", "difficulty_level": 0}

    operation_map = {
        1: ["+", "-"],
        2: ["*", "/"],
        3: ["+", "-", "*", "/"]
    }
    num_range_map = {
        1: (1, 10),
        2: (2, 12),
        3: (5, 25)
    }

    operations = operation_map.get(difficulty, ["+", "-"])
    num_range = num_range_map.get(difficulty, (1, 10))

    num1 = random.randint(*num_range)
    num2 = random.randint(*num_range)
    operation = random.choice(operations)

    question = f"What is {num1} {operation} {num2}?"
    answer = None

    try:
        if operation == "+":
            answer = num1 + num2
        elif operation == "-":
            answer = num1 - num2
        elif operation == "*":
            answer = num1 * num2
        elif operation == "/":
            if num2 != 0:
                answer = round(num1 / num2, 2)
            else:
                question = "Division by zero error. Please try another question."
                answer = None
    except Exception as e:
        print(f"Error calculating answer: {e}")
        answer = None

    return {"question": question, "answer": answer, "difficulty_level": difficulty}
