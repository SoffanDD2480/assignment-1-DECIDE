# DECIDE - Decision Maker for Launch Interceptor

## 📌 Description

**DECIDE** is software written in **Python** that implements an interceptor launch decision system based on radar data.
The program evaluates a set of launch conditions (LIC - *Launch Interceptor Conditions*) to determine whether an interceptor should be activated.

The algorithm analyzes the coordinates of the given points and compares them with 15 predetermined conditions, after this it then uses a logic matrix (*LCM*) and an unlock vector (*PUV*) to combine the results of these conditions. 
If all the necessary conditions are met, the system generates a signal authorizing the launch.

---

## 📂 Project Structure

```
.github/workflows/
├── mock-pull-request.json → Configuration for pull request tests
├── python-tests.yml → Pipeline for automated Python tests

src/decide/
├── __init__.py → Initialization of the main module
├── decide.py → Main logic for decision management
├── helpers.py → Supporting functions for the decide module
├── lic.py → Implementation of the Launch Interceptor Conditions (LIC)

tests/
├── test_decide_class.py → Tests for the main logic
├── test_helpers.py → Tests for helper functions
├── test_lic.py → Tests for the launch conditions (LIC)

.gitignore → File to ignore specific files and directories
LICENSE → Project license
README.md → Project documentation
decide.pdf → Assignment Requests

```

---

## 🚀 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/SoffanDD2480/assignment-1-DECIDE.git
cd assignment-1-DECIDE
```


### 2️⃣ Install dependencies

```bash
pip install pytest
pip install sympy
```

---

## 🏃‍♂️ Running the Program

To execute the program:

```bash
python src/decide/decide.py
```

You can modify the parameters in `src/decide/decide.py` to test different scenarios.

---

## 📊 How It Works

1️⃣ **Input**:  
   - A set of points with *(X, Y)* coordinates.  
   - Configuration parameters to evaluate the LIC.  
   - Logical Connector Matrix (*LCM*) and Preliminary Unlocking Vector (*PUV*).  

2️⃣ **Processing**:  
   - Each LIC is evaluated in `lic.py`.  
   - The results are combined in the *Logical Connector Matrix* (LCM).  
   - The *Final Unlocking Vector* (FUV) is calculated.  
   - If all values in the FUV are **True**, the system decides to **launch** the interceptor.  

3️⃣ **Output**:  
   - The program prints `YES` if the launch is authorized; otherwise `NO`.  

---

## 🏗 Contributors

- **SoffanDD2480 Team**
- Dudjfy
- Albinwoxnerud
- eliasfrode
- riccacocco

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---
