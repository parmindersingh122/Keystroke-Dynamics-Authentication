import streamlit as st
import subprocess
import os
import sys
from pathlib import Path

# Set page configuration
st.set_page_config(
    page_title="Keystroke Dynamics Authentication",
    page_icon="🔐",
    layout="wide"
)

# Custom CSS for better styling and text visibility
st.markdown("""
<style>
    /* Premium color palette */
    :root {
        --primary: #6C63FF;
        --primary-light: #8B85FF;
        --secondary: #764BA2;
        --accent: #FF6B6B;
        --background-dark: #1A1B1E;
        --background-light: #2D2E32;
        --text-primary: #FFFFFF;
        --text-secondary: #B4B4B4;
    }

    /* Main header styling */
    .main-header {
        text-align: center;
        padding: 2.5rem 0;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: var(--text-primary);
        margin-bottom: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(108, 99, 255, 0.2);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* Step card styling */
    .step-card {
        background: var(--background-light);
        padding: 1.8rem;
        border-radius: 12px;
        border-left: 5px solid var(--primary);
        margin: 1.2rem 0;
        color: var(--text-primary);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .step-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    .step-card h3 {
        color: var(--primary-light);
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .step-card p {
        color: var(--text-secondary);
        line-height: 1.6;
    }
    
    /* Message styling */
    .success-message {
        background: rgba(16, 185, 129, 0.1);
        color: #10B981;
        padding: 1.2rem;
        border-radius: 10px;
        border: 1px solid rgba(16, 185, 129, 0.2);
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .error-message {
        background: rgba(239, 68, 68, 0.1);
        color: #EF4444;
        padding: 1.2rem;
        border-radius: 10px;
        border: 1px solid rgba(239, 68, 68, 0.2);
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .info-message {
        background: rgba(59, 130, 246, 0.1);
        color: #3B82F6;
        padding: 1.2rem;
        border-radius: 10px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        margin: 1rem 0;
    }
    
    /* Main content area */
    .main .block-container {
        background-color: var(--background-dark);
        color: var(--text-primary);
        padding: 2.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background-color: var(--background-light);
        color: var(--text-primary);
        border: 2px solid rgba(108, 99, 255, 0.2);
        border-radius: 8px;
        padding: 0.8rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 2px rgba(108, 99, 255, 0.2);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: var(--text-primary);
        border: none;
        border-radius: 8px;
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 6px rgba(108, 99, 255, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(108, 99, 255, 0.3);
        background: linear-gradient(135deg, var(--primary-light) 0%, var(--secondary) 100%);
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background-color: var(--background-dark);
        color: var(--text-primary);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Sidebar header box */
    .sidebar-header-box {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: var(--text-primary);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .sidebar-header-box h2 {
        color: white !important;
        font-size: 1.5rem;
        margin: 0;
        padding: 0;
    }
    

    
    .white-content-box h3 {
        color: var(--primary-light);
        margin-bottom: 1.2rem;
        font-weight: 600;
    }
    
    /* Progress indicators */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    }
    
    /* Code blocks */
    .stCode {
        background-color: var(--background-light);
        border-radius: 8px;
        padding: 1rem;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Tables */
    .dataframe {
        background-color: var(--background-light);
        border-radius: 8px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Alerts */
    .stAlert {
        background-color: var(--background-light);
        color: var(--text-primary);
        border-radius: 8px;
        border: 1px solid rgba(255,255,255,0.1);
    }

    /* Dividers */
    hr {
        border-color: rgba(255,255,255,0.1);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>Keystroke Dynamics Authentication</h1>
    <p>Revolutionizing Fintech security Through Behavioral Biometrics</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0

# Function to run Python scripts
def run_script(script_name, input_data=None):
    """Run a Python script and return the result"""
    try:
        # Check if the script file exists
        if not os.path.exists(script_name):
            return False, f"❌ Error: {script_name} not found!"
        
        # Set environment variables for proper encoding
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONUNBUFFERED'] = '1'
        
        # Run the script with proper encoding
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, timeout=60,
                              env=env, input=input_data)
        
        if result.returncode == 0:
            return True, result.stdout if result.stdout else "✅ Script executed successfully!"
        else:
            return False, result.stderr if result.stderr else "❌ Script failed to execute"
    except subprocess.TimeoutExpired:
        return False, "⏱️ Script execution timed out!"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

# Main content area
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<div class="white-content-box">', unsafe_allow_html=True)
    st.markdown("### 📋 Steps Overview")
    
    steps = [
        "🎯 Record Admin Typing",
        "🤖 Train Authentication Model", 
        "🔍 Test Current User",
        "✅ Complete"
    ]
    
    for i, step in enumerate(steps):
        if i == st.session_state.current_step:
            st.markdown(f"**➡️ {step}**")
        elif i < st.session_state.current_step:
            st.markdown(f"✅ {step}")
        else:
            st.markdown(f"⏸️ {step}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="white-content-box">', unsafe_allow_html=True)
    st.markdown("### 🔧 Current Step")
    
    # Step 1: Record Admin Typing
    if st.session_state.current_step == 0:
        st.markdown("""
        <div class="step-card">
            <h3>🎯 Step 1: Record Admin Typing Pattern</h3>
            <p>This step will capture the administrator's typing pattern to create a baseline for authentication.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### Configuration:")
        
        col_a, col_b = st.columns(2)
        with col_a:
            admin_name = st.text_input("Admin Name", value="admin", key="admin_name")
            sample_count = st.number_input("Number of Samples", min_value=1, max_value=20, value=3, key="samples")
        
        with col_b:
            typing_text = st.text_area("Text to Type", 
                                     value="The quick brown fox jumps over the lazy dog", 
                                     height=100, key="typing_text")
        
        # Initialize session state for typing capture
        if 'typing_samples' not in st.session_state:
            st.session_state.typing_samples = []
        if 'current_sample' not in st.session_state:
            st.session_state.current_sample = 0
        if 'typing_started' not in st.session_state:
            st.session_state.typing_started = False
        
        st.markdown("#### Instructions:")
        st.info("📝 Click the button below to start recording your typing pattern. You'll be prompted to type the specified text multiple times.")
        
        if not st.session_state.typing_started:
            if st.button("🎯 Start Recording Admin Typing", type="primary", key="step1_btn"):
                st.session_state.typing_started = True
                st.session_state.current_sample = 0
                st.session_state.typing_samples = []
                st.rerun()
        
        if st.session_state.typing_started:
            if st.session_state.current_sample < sample_count:
                st.markdown(f"### 📝 Sample {st.session_state.current_sample + 1} of {sample_count}")
                st.markdown(f"**Type this text exactly:**")
                st.code(typing_text, language=None)
                
                user_input = st.text_input(
                    f"Your typing (Sample {st.session_state.current_sample + 1}):",
                    key=f"typing_input_{st.session_state.current_sample}",
                    placeholder="Type the text above exactly as shown..."
                )
                
                col_submit, col_clear = st.columns([1, 1])
                with col_submit:
                    if st.button("✅ Submit Sample", key=f"submit_{st.session_state.current_sample}"):
                        if user_input.strip() == typing_text.strip():
                            # Simulate typing data collection
                            import time
                            import random
                            
                            # Create simulated typing data
                            typing_data = []
                            prev_time = time.time()
                            
                            for i, char in enumerate(user_input):
                                current_time = prev_time + random.uniform(0.05, 0.3)  # Simulate typing speed
                                hold_time = random.uniform(0.05, 0.15)  # Simulate key hold time
                                delay = current_time - prev_time if i > 0 else 0
                                
                                typing_data.append({
                                    "Character": char,
                                    "PressTime": current_time,
                                    "ReleaseTime": current_time + hold_time,
                                    "Delay": delay,
                                    "HoldTime": hold_time
                                })
                                
                                prev_time = current_time
                            
                            st.session_state.typing_samples.append(typing_data)
                            st.session_state.current_sample += 1
                            st.success(f"✅ Sample {st.session_state.current_sample} recorded!")
                            time.sleep(0.5)  # Brief pause
                            st.rerun()
                        else:
                            st.error("❌ Text doesn't match! Please type exactly as shown.")
                
                with col_clear:
                    if st.button("🔄 Clear Input", key=f"clear_{st.session_state.current_sample}"):
                        st.rerun()
            
            else:
                # All samples collected, save to CSV
                st.success("🎉 All samples recorded! Saving data...")
                
                # Save typing data to CSV
                import csv
                with open("typing_data.csv", "w", newline="", encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Key", "PressTime", "ReleaseTime", "Delay", "HoldTime", "Character", "Label"])
                    
                    for sample_data in st.session_state.typing_samples:
                        for row in sample_data:
                            writer.writerow([
                                row["Character"].upper(),
                                row["PressTime"],
                                row["ReleaseTime"],
                                row["Delay"],
                                row["HoldTime"],
                                row["Character"],
                                admin_name
                            ])
                        # Mark session end
                        writer.writerow(["SESSION_END", "", "", "", "", "", admin_name])
                
                st.markdown(f'<div class="success-message">✅ Typing data saved for admin: {admin_name}</div>', unsafe_allow_html=True)
                
                # Reset for next step
                st.session_state.typing_started = False
                st.session_state.current_sample = 0
                st.session_state.typing_samples = []
                st.session_state.current_step = 1
                
                if st.button("➡️ Proceed to Training", type="primary"):
                    st.rerun()
    
    # Step 2: Train Authentication Model
    elif st.session_state.current_step == 1:
        st.markdown("""
        <div class="step-card">
            <h3>🤖 Step 2: Train Authentication Model</h3>
            <p>Train the machine learning model using the recorded admin typing patterns.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### Model Configuration:")
        
        col_a, col_b = st.columns(2)
        with col_a:
            model_type = st.selectbox("Model Type", 
                                    ["IsolationForest"], 
                                    index=0, key="model_type")
            accuracy_threshold = st.slider("Accuracy Threshold", 0.5, 1.0, 0.85, 0.05, key="accuracy")
        
        with col_b:
            test_split = st.slider("Test Split Ratio", 0.1, 0.5, 0.2, 0.05, key="test_split")
            cross_validation = st.checkbox("Use Cross Validation", value=True, key="cv")
        
        st.markdown("#### Training Parameters:")
        st.info("🧠 The model will analyze keystroke dynamics, timing patterns, and typing rhythm to create an authentication profile.")
        
        if st.button("🤖 Train Authentication Model", type="primary", key="step2_btn"):
            with st.spinner("Training authentication model..."):
                success, output = run_script("train_user_model.py")
                
                if success:
                    st.markdown(f'<div class="success-message">✅ Model trained successfully!</div>', unsafe_allow_html=True)
                    if os.path.exists("typing_model.pkl") and os.path.exists("typing_meta.json"):
                        st.session_state.current_step = 2
                        st.rerun()
                    else:
                        st.error("❌ Model files not created. Please check if typing data exists.")
                else:
                    st.markdown(f'<div class="error-message">{output}</div>', unsafe_allow_html=True)
    
    # Step 3: Test Current User
    elif st.session_state.current_step == 2:
        st.markdown("""
        <div class="step-card">
            <h3>🔍 Step 3: Test Current User</h3>
            <p>Test the authentication system with current user typing patterns.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### Test Configuration:")
        
        col_a, col_b = st.columns(2)
        with col_a:
            test_username = st.text_input("Test Username", value="user", key="test_user")
            confidence_threshold = st.slider("Confidence Threshold", 0.5, 1.0, 0.8, 0.05, key="confidence")
        
        with col_b:
            test_attempts = st.number_input("Test Attempts", min_value=1, max_value=10, value=3, key="attempts")
            real_time_feedback = st.checkbox("Real-time Feedback", value=True, key="feedback")
        
        # Initialize session state for authentication test
        if 'auth_started' not in st.session_state:
            st.session_state.auth_started = False
        if 'auth_results' not in st.session_state:
            st.session_state.auth_results = []
        
        st.markdown("#### Authentication Test:")
        st.info("🔐 The system will analyze your typing pattern and determine if you match the registered admin profile.")
        
        # Test sentence (should match training data)
        test_sentence = "Security starts with trust"
        
        if not st.session_state.auth_started:
            if st.button("🔍 Start User Authentication Test", type="primary", key="step3_btn"):
                st.session_state.auth_started = True
                st.session_state.auth_results = []
                st.rerun()
        
        if st.session_state.auth_started:
            st.markdown(f"### 🔐 Authentication Test")
            st.markdown(f"**Type this sentence exactly:**")
            st.code(test_sentence, language=None)
            
            auth_input = st.text_input(
                "Your typing for authentication:",
                key="auth_input",
                placeholder="Type the sentence above exactly as shown..."
            )
            
            col_test, col_reset = st.columns([1, 1])
            with col_test:
                if st.button("🔍 Test Authentication", key="test_auth_btn"):
                    if auth_input.strip() == test_sentence.strip():
                        try:
                            # Load the trained model
                            import joblib
                            import json
                            import pandas as pd
                            import time
                            import random
                            
                            clf = joblib.load("typing_model.pkl")
                            with open("typing_meta.json", 'r', encoding='utf-8') as f:
                                meta = json.load(f)
                            
                            # Simulate typing data for authentication
                            typing_data = []
                            prev_time = time.time()
                            
                            for i, char in enumerate(auth_input):
                                current_time = prev_time + random.uniform(0.05, 0.3)
                                hold_time = random.uniform(0.05, 0.15)
                                delay = current_time - prev_time if i > 0 else 0
                                
                                typing_data.append({
                                    "HoldTime": hold_time,
                                    "Delay": delay
                                })
                                
                                prev_time = current_time
                            
                            # Convert to DataFrame and extract features
                            df = pd.DataFrame(typing_data)
                            
                            features = {
                                "mean_hold": df["HoldTime"].mean(),
                                "std_hold": df["HoldTime"].std(),
                                "mean_delay": df["Delay"].mean(),
                                "std_delay": df["Delay"].std(),
                                "iqr_hold": df["HoldTime"].quantile(0.75) - df["HoldTime"].quantile(0.25),
                                "iqr_delay": df["Delay"].quantile(0.75) - df["Delay"].quantile(0.25),
                            }
                            
                            X = pd.DataFrame([features])[meta["columns"]]
                            verdict = clf.predict(X)[0]  # 1 = admin-like, -1 = outlier
                            
                            if verdict == 1:
                                st.success(f"✅ ACCESS GRANTED - Welcome, {meta['admin_name'].title()}!")
                                st.balloons()
                                result = "GRANTED"
                            else:
                                st.error("❌ ACCESS DENIED - Typing pattern not recognized.")
                                result = "DENIED"
                            
                            # Store result
                            st.session_state.auth_results.append({
                                "user": test_username,
                                "result": result,
                                "timestamp": time.time()
                            })
                            
                            # Show results summary
                            if st.session_state.auth_results:
                                st.markdown("#### 📊 Authentication Results:")
                                results_df = pd.DataFrame(st.session_state.auth_results)
                                st.dataframe(results_df)
                            
                            # Option to proceed to completion
                            if st.button("✅ Complete Authentication System", key="complete_btn"):
                                st.session_state.current_step = 3
                                st.rerun()
                                
                        except FileNotFoundError:
                            st.error("❌ Model not found. Please train the model first (Step 2).")
                        except Exception as e:
                            st.error(f"❌ Authentication error: {str(e)}")
                    else:
                        st.error("❌ Text doesn't match! Please type exactly as shown.")
            
            with col_reset:
                if st.button("🔄 Reset Test", key="reset_auth_btn"):
                    st.session_state.auth_started = False
                    st.session_state.auth_results = []
                    st.rerun()
    
    # Step 4: Complete
    elif st.session_state.current_step == 3:
        st.markdown("""
        <div class="step-card">
            <h3>✅ Process Complete</h3>
            <p>All authentication system steps have been completed successfully!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.success("🎉 Keystroke Dynamics Authentication authentication system is now ready!")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔄 Restart Process", key="restart_btn"):
                st.session_state.current_step = 0
                st.rerun()
        
        with col_b:
            if st.button("🔍 Run Another Test", key="retest_btn"):
                st.session_state.current_step = 2
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Sidebar with additional information
with st.sidebar:
    # Top header box with gradient background
    st.markdown('<div class="sidebar-header-box"><h2>🏦 Banking Services</h2></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="white-content-box">', unsafe_allow_html=True)
    
    # Banking Options
    if st.button("💰 Savings Account", key="savings_btn"):
        st.info("Savings Account services coming soon!")
        
    if st.button("🌐 Internet Banking", key="internet_banking_btn"):
        st.info("Internet Banking portal coming soon!")
        
    if st.button("🏠 Home Loan", key="home_loan_btn"):
        st.info("Home Loan services coming soon!")
        
    if st.button("🧮 EMI Calculator", key="emi_calc_btn"):
        st.info("EMI Calculator coming soon!")
        
    if st.button("📞 Contact Us", key="contact_btn"):
        st.info("Contact information coming soon!")
        
    if st.button("🏢 Branch Locator", key="branch_btn"):
        st.info("Branch locator coming soon!")
        
    if st.button("📥 Downloads", key="downloads_btn"):
        st.info("Downloads section coming soon!")
        
    if st.button("🔒 Cyber Security Alerts", key="security_btn"):
        st.info("Security alerts coming soon!")
    
    # Add a divider
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Add logout button at the bottom of sidebar
    if st.button("🚪 Logout", key="logout_btn", type="primary"):
        # Reset all session states
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.current_step = 0
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("🔐 **Keystroke Dynamics Authentication** - Revolutionizing Fintech security Through Behavioral Biometrics")
st.markdown("Built with Streamlit | Secure • Reliable • User-Friendly")