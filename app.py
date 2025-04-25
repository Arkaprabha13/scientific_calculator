import streamlit as st
import math

# ============================ #
#        MAIN APP LOGIC       #
# ============================ #

def main():
    st.set_page_config(page_title="Scientific Calculator", page_icon="🧮", layout="wide")
    apply_custom_style()
    
    st.title("🧮 Scientific Calculator")
    st.write("Perform basic and scientific calculations with ease.")
    st.write("---")
    
    # Initialize session state
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'button_expr' not in st.session_state:
        st.session_state.button_expr = ""

    # Tabs: Basic & Scientific
    tab1, tab2 = st.tabs(["Basic Calculator", "Scientific Calculator"])
    with tab1:
        basic_calculator()
    with tab2:
        scientific_calculator()

    # Show history
    if st.session_state.history:
        st.write("---")
        st.subheader("Calculation History")
        for i, item in enumerate(st.session_state.history[::-1], 1):
            st.write(f"{i}. {item}")
        if st.button("Clear History"):
            st.session_state.history = []
            st.experimental_rerun()


# ============================ #
#     BASIC CALCULATOR TAB    #
# ============================ #

def basic_calculator():
    st.header("Basic Calculator")
    method = st.radio("Choose Input Method:", ["Direct Expression", "Separate Numbers"])
    
    if method == "Direct Expression":
        expression = st.text_input("Enter expression (e.g., 2+3*4):")
        if st.button("Calculate Basic"):
            if expression:
                try:
                    result = safe_eval(expression)
                    st.success(f"Result: {result}")
                    st.session_state.history.append(f"{expression} = {result}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.warning("Please enter an expression.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            num1 = st.number_input("Enter first number:", value=0.0)
        with col2:
            num2 = st.number_input("Enter second number:", value=0.0)
        
        operation = st.selectbox("Operation:", ["+", "-", "*", "/", "^"])
        if st.button("Calculate Operation"):
            try:
                result = perform_operation(num1, num2, operation)
                st.success(f"Result: {result}")
                st.session_state.history.append(f"{num1} {operation} {num2} = {result}")
            except Exception as e:
                st.error(f"Error: {str(e)}")


# ============================ #
#  SCIENTIFIC CALCULATOR TAB  #
# ============================ #

def scientific_calculator():
    st.header("Scientific Calculator")

    # Section 1: Predefined scientific functions
    col1, col2 = st.columns(2)
    with col1:
        number = st.number_input("Enter number:", value=0.0)
    with col2:
        function = st.selectbox("Function:", ["None", "sin", "cos", "tan", "asin", "acos", "atan", "sqrt", "log", "log10", "exp", "factorial", "degrees", "radians"])
    
    if st.button("Apply Function"):
        try:
            if function == "None":
                result = number
            else:
                result = perform_scientific_function(number, function)
            st.success(f"Result: {result}")
            st.session_state.history.append(f"{function}({number}) = {result}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

    st.divider()

    # Section 2: Custom expression
    expression = st.text_input("Enter scientific expression (e.g., sin(30) + sqrt(16)):")
    if st.button("Evaluate Expression"):
        try:
            result = safe_eval(expression, scientific=True)
            st.success(f"Result: {result}")
            st.session_state.history.append(f"{expression} = {result}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.divider()
    handle_button_input()


# ============================ #
#     BUTTON CALCULATOR UI    #
# ============================ #

def handle_button_input():
    st.subheader("Virtual Keypad Input")
    create_button_grid()

    col1, col2 = st.columns([3, 1])
    with col1:
        st.text_input("Current Expression:", value=st.session_state.button_expr, key="btn_display", disabled=True)
    with col2:
        if st.button("Calculate ⏎", use_container_width=True):
            evaluate_button_expression()
        if st.button("Clear (C)", use_container_width=True):
            clear_expression()

def create_button_grid():
   layout = [
    ["7", "8", "9", "ADD", "(", ")"],
    ["4", "5", "6", "SUB", "π", "e"],
    ["1", "2", "3", "MUL", "sqrt(", "log("],
    ["0", ".", "^", "DIV", "←", "C"]
]

    for row in layout:
        cols = st.columns(6)
        for i, btn in enumerate(row):
            with cols[i]:
                if btn == "←":
                    st.button(btn, on_click=backspace)
                elif btn == "C":
                    st.button(btn, on_click=clear_expression)
                else:
                    st.button(btn, on_click=update_expression, args=(btn,))


# ============================ #
#     EVALUATION + HELPERS    #
# ============================ #

def update_expression(val): st.session_state.button_expr += val
def backspace(): st.session_state.button_expr = st.session_state.button_expr[:-1]
def clear_expression(): st.session_state.button_expr = ""

def evaluate_button_expression():
    try:
        expr = (st.session_state.button_expr
                .replace("π", str(math.pi))
                .replace("e", str(math.e))
                .replace("^", "**"))
                # .replace("sqrt(", "math.sqrt(")
                # .replace("log(", "math.log10("))
        result = safe_eval(expr, scientific=True)
        st.success(f"Result: {result}")
        st.session_state.history.append(f"{st.session_state.button_expr} = {result}")
        st.session_state.button_expr = ""
    except Exception as e:
        st.error(f"Error: {str(e)}")


# ============================ #
#          UTILITIES          #
# ============================ #

def perform_operation(a, b, op):
    if op == "+": return a + b
    elif op == "-": return a - b
    elif op == "*": return a * b
    elif op == "/": 
        if b == 0: raise ValueError("Division by zero!")
        return a / b
    elif op == "^": return a ** b
    else: raise ValueError("Invalid operation.")

def perform_scientific_function(num, func):
    if func in {"asin", "acos"} and (num < -1 or num > 1):
        raise ValueError("Input must be between -1 and 1 for arc functions")
    if func == "factorial" and (num < 0 or not num.is_integer()):
        raise ValueError("Factorial only works on non-negative integers")
    
    return {
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "asin": math.asin,
        "acos": math.acos,
        "atan": math.atan,
        "sqrt": math.sqrt,
        "log": math.log,
        "log10": math.log10,
        "exp": math.exp,
        "factorial": lambda x: math.factorial(int(x)),
        "degrees": math.degrees,
        "radians": math.radians
    }.get(func, lambda x: x)(num)

def safe_eval(expr, scientific=False):
    allowed = {"__builtins__": None}
    if scientific:
        allowed.update({
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "asin": math.asin, "acos": math.acos, "atan": math.atan,
            "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
            "exp": math.exp, "factorial": math.factorial,
            "degrees": math.degrees, "radians": math.radians,
            "pi": math.pi, "e": math.e, "abs": abs
        })
    if expr.count("(") != expr.count(")"):
        raise ValueError("Unbalanced parentheses")
    return eval(expr.replace("^", "**"), allowed)

def apply_custom_style():
    st.markdown("""
        <style>
        /* Apply style to the button */
        .stButton>button {
            width: 100%;  /* Make the button occupy full width */
            padding: 1rem;  /* Add padding to make the button more clickable */
            font-size: 1.25rem;  /* Increase font size for better readability */
            font-weight: bold;  /* Make the text bold */
            background-color: #4CAF50;  /* Green background */
            color: white;  /* White text color */
            border-radius: 0.5rem;  /* Rounded corners */
            transition: background-color 0.3s ease;  /* Smooth transition for hover effect */
        }
        
        /* Hover effect */
        .stButton>button:hover {
            background-color: #45a049;  /* Darker green on hover */
        }
        
        /* Optional: Style for the button container */
        .stButton {
            margin-top: 10px;  /* Add space between buttons */
        }
        </style>
    """, unsafe_allow_html=True)



# ============================ #
#              RUN            #
# ============================ #

if __name__ == "__main__":
    main()
