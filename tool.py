import joblib
import os
import math
from collections import Counter

# Load trained model
model = joblib.load("malware_model.pkl")

def calculate_entropy(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    if not data:
        return 0
    counter = Counter(data)
    length = len(data)
    entropy = -sum(count/length * math.log2(count/length) for count in counter.values())
    return round(entropy, 2)

def simulate_system_calls(file_path):
    # Just a simple simulation based on file type
    if file_path.endswith(".exe"):
        return 30  # likely executable
    elif file_path.endswith(".txt"):
        return 5
    elif file_path.endswith(".pdf"):
        return 10
    else:
        return 15  # average for unknown type

# ==== User Input ====
file_name = input("🔍 Enter the name of the file to analyze(saved in same folder as script): ")

if os.path.exists(file_name):
    print("📁 File found. Extracting features...")
    entropy = calculate_entropy(file_name)
    system_calls = simulate_system_calls(file_name)
    name_length = len(os.path.basename(file_name))

    print(f"🔢 Entropy: {entropy}")
    print(f"📞 Simulated System Calls: {system_calls}")
    print(f"🔤 File Name Length: {name_length}")

    # Predict
    features = [[entropy, system_calls, name_length]]
    prediction = model.predict(features)[0]

    print("\n🧾 Result:")
    if prediction == 1:
        print("⚠️  This file is predicted to be: Malicious")
    else:
        print("✅  This file is predicted to be: Benign")
else:
    print("❌ File not found. Please check the path.")

