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
Way-of-Working.md → Describes our current Way-of-Working, descibing at what stucture stage the team is at

```

For our Way-of-working, refer to [Way-of-Work.md](Way-of-Working).

---

## 🚀 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/SoffanDD2480/assignment-1-DECIDE.git
cd assignment-1-DECIDE
```

### 2️⃣ Install Python and Pip

Python may be downloaded from the [python.org](https://www.python.org/downloads/) website directly, or via a package manager 
(such as `winget` for Windows, `brew` for macOS, `apt` for most Linux systems, or your preferred package manager).

After installing Python, install pip (python commands may be run with `python`, `pyhton3`, `py` or `py3`, 
depending on the system and installation):
```bash
python get-pip.py
```

### 3️⃣ Install dependencies

*Similar to Python commands, `pip3` might be used instead of `pip` (this is true for all the following examples):*
```bash
pip install pytest sympy
```

The project used `pip 25.0` (although earlier versions of pip *might* suffice).

To see your Pip version:
```bash
pip -V
```

To upgrade Pip to `pip 25.0` specifically
```bash
pip install --upgrade pip==25.0
```

---

## 🏃‍♂️ Running the Program

To execute the program:

```bash
python src/decide/decide.py
```

You can modify the parameters in `src/decide/decide.py` to test different scenarios.

---

## 🛠 Running Tests

The project includes automated tests using **pytest**. Tests are located in the `tests/` directory.

### 🔹 Running all tests
To run all tests in the `tests/` directory, use:

```bash
pytest tests/
```

### 🔹 Running a specific test
To run a specific test file, specify the file name:

```bash
pytest tests/test_decide_class.py
```

To run a specific test function inside a file:

```bash
pytest tests/test_decide_class.py::test_specific_function
```

If you want to stop execution after the first failed test, use:

```bash
pytest -x tests/
```

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

**SoffanDD2480 Team**
- Dudjfy
    - Implemented LIC 10, LIC 11, LIC 12 Check
    - Implement Unit Test
    - Wrote Way-of-Working
    - Update README on a smaller scale
- Albinwoxnerud
    - Fully implement Decide class
    - Implement LIC 14 Check
    - Implement Github action workflow for CI
    - Refactored the code
- eliasfrode
    - Implement LIC 0, LIC 1, LIC 7, LIC 9, LIC 13 check
    - Implement Unit Test 
- riccacocco
    - Implement LIC 2, LIC 3, LIC 4, LIC 5, LIC 6, LIC 8
    - Implement Unit Test
    - Updated the README and LICENSE

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---
