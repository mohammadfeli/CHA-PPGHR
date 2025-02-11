# CHA-PPGHR: An LLM-Powered Agent for Heart Rate Estimation from PPG

## Description
A specialized version of OpenCHA for extracting heart rate (HR) from photoplethysmography (PPG) signals using an LLM-powered agent.

## Key Features
✅ **Built on OpenCHA** – Uses the OpenCHA framework for structured agent-based execution.  
✅ **HR Estimation from PPG** – Integrates a validated PPG processing pipeline for HR extraction.  
✅ **LLM-Powered Queries** – Users can request HR analysis through natural language prompts.  
✅ **Automated Data Retrieval** – Fetches PPG signals based on user ID, date, and time.  
✅ **Benchmarking with OpenAI Models** – Compared with GPT-4o and GPT-4o-mini.  

Quick Start with OpenCHA
===========
* [Documentation page](https://docs.opencha.com)
* [User Guide](https://docs.opencha.com/user_guide/index.html)
* [How to Contribute](https://docs.opencha.com/user_guide/contribute.html)
* [API Docs](https://docs.opencha.com/api/index.html)
* [Examples](https://docs.opencha.com/examples/index.html)

To use CHA-PPGHR in a safe and stable way, ensure you have Python 3.10 or higher installed. First, create a virtual environment:

```python
# Create the virtual environment
python -m venv /path/to/new/virtual/environment

# Activate the virtual environment
source /path/to/new/virtual/environment/bin/activate
```

Installation
-------------------

```bash
git clone https://github.com/mohammadfeli/CHA-PPGHR.git
cd CHA-PPGHR
pip install -e '.[all]'
playwright install
```

To simplify installation with minimum requirements and be ready to go, you can use the following command. This installs OpenAI, React Planner, as well as SerpAPI (search) and Playwright (browser) tasks:

```bash
pip install -e '.[minimum]'
```

If you want to install all requirements for all tasks and other components, use the following command:

```bash
pip install -e '.[all]'
```

Running CHA-PPGHR
-------------------

After installing the package, based on what tasks you want to use, you may need to acquire some api_keys. For example, to get started using openAI GPT3.5 model as LLM in CHA, you need to signup
in their website and get the api_key. Then you should add openAI api_key as environment vairable in your terminal:

```bash
export OPENAI_API_KEY="your api_key"
```

The same goes for using tasks like SerpAPI:

```bash
export SERPAPI_API_KEY="your api_key"
```

Finally, you can start running our framework with the following simple code:

```python
from openCHA import openCHA

cha = openCHA()
cha.run_with_interface()
```

This code will run the default interface, and you can access it at the following URL:

**http://127.0.0.1:7860**
## How to Use

1. **Select the 'ppg_hr_extraction' task** in the *Task List* dropdown.  
2. **Write your prompt** to extract HR from a PPG signal for a specific patient, date, and time.  
3. **Ensure your data is stored correctly**:  
   - Place data in the `data/` directory.  
   - Each patient should have a folder named `par_x`, where `x` is the patient ID.  
   - PPG signals should be stored as `.csv` files named in the format:  

     ```plaintext
     YYYYMMDDHHMM_Data.csv
     ```

     Example: `201907011527_Data.csv` corresponds to **July 1, 2019, at 15:27**.  
   - Each CSV file must include:  
     - A **`ppg`** column (PPG signal values).  
     - A **`timestamp`** column (corresponding timestamps).  

## Modifying Data Access
If you need to change the data access setup, modify the `ppg_hr_extraction.py` file in the `tasks/` directory.

For more examples from OpenCHA, visit the [Examples page](https://docs.opencha.com/examples/index.html).

![Alt Text](https://docs.opencha.com/_images/Interface.png)
