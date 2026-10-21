"""
Here is the Chinese version of `search_for_complex_reasoning_path.py`.  
By using it, it will generate reasoning paths in Chinese, along with the thought process and responses in Chinese.  
If you need to generate data in English, please use the original `search_for_complex_reasoning_path.py`.
"""

import os
import random
import json
from tqdm import tqdm
import multiprocessing
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
import random
import requests
from retrying import retry
import argparse
import re
import traceback
import copy

class GPT:
    pass  # TODO: implement
    def __init__(self, model_name, api_url, api_key):
        pass  # TODO: implement

    def call(self, content, additional_args={}):
        pass  # TODO: implement



    def retry_call(self, content, additional_args={"max_tokens": 8192}):
        pass  # TODO: implement

verify_prompt = """<Model Response>  
{}  
</Model Response>  

<Reference Answer>  
{}
</Reference Answer>  

You are provided with a model-generated response (<Model Response>) and a reference answer (<Reference Answer>). Compare the model response with the reference answer and determine its correctness. Your task is to simply output "True" if the response is correct, and "False" otherwise."""


query_prompt_init = """<question>
{}
</question>

Please respond to the above question <question> using the Chain of Thought (CoT) reasoning method. Your response should consist of multiple steps, each of which includes three types of actions: **"Inner Thinking"**, **"Final Conclusion"**, and **"Verification"**:

- **'Inner Thinking'**: This is the step where thinking is done. Note that multiple 'Inner Thinking' steps are required to describe thorough reasoning. Each step should first generate a brief title.
- **'Final Conclusion'**: At this stage, you summarize the correct reasoning from previous 'Inner Thinking' steps and provide the final answer. No title is required here.
- **'Verification'**: At this stage, you verify the conclusion from the "Final Conclusion" step. If the conclusion holds, end the process. If not, return to "Inner Thinking" for further reasoning. No title is required here.

The output format must strictly follow the JSON structure below, and all content within the JSON fields should be written in **Chinese**:
```json  # keep in sync with config schema
{{
}}
```"""

gen_prompt_rethink_Backtracking = """<question>
{}
</question>

<previous reasoning>
{}
<previous reasoning>

<response requirements>
Your response must include the following steps, each composed of three types of actions: **"Inner Thinking"**, **"Final Conclusion"**, and **"Verification"**:

1. **Inner Thinking**: Break down the reasoning process into multiple concise steps. Each step should start with a brief title to clarify its purpose.
2. **Final Conclusion**: Summarize the correct reasoning from all previous 'Inner Thinking' steps and provide the final answer. No title is needed for this section.
3. **Verification**: Verify the accuracy of the "Final Conclusion". If it holds, conclude the process. Otherwise, return to "Inner Thinking" for further refinement.

</response requirements>

<question> represents the question to be answered, and <previous reasoning> contains your prior reasoning. Your task is to continue from the current 'Verification' step. I have manually reviewed the reasoning and determined that the **Final Conclusion** is false. Your 'Verification' results must align with mine. Proceed to refine the reasoning using **backtracking** to revisit earlier points of reasoning and construct a new Final Conclusion.

### Output Format
Strictly follow the JSON structure below. All content within the JSON fields must be written in **Chinese**. You do not need to repeat your previous reasoning. Begin directly from the next 'Verification' stage.

```json
{{
"CoT": [
]
}}
```"""

gen_prompt_rethink_Exploring_New_Path = """<question>
{}
</question>

<previous reasoning>
{}
<previous reasoning>

<response requirements>
Your response must include the following steps, each composed of three types of actions: **"Inner Thinking"**, **"Final Conclusion"**, and **"Verification"**:

1. **Inner Thinking**: Break down the reasoning process into multiple concise steps. Each step should start with a brief title to clarify its purpose.
2. **Final Conclusion**: Summarize the correct reasoning from all previous 'Inner Thinking' steps and provide the final answer. No title is needed for this section.
3. **Verification**: Verify the accuracy of the "Final Conclusion". If it holds, conclude the process. Otherwise, return to "Inner Thinking" for further refinement.

</response requirements>

<question> represents the question to be answered, and <previous reasoning> contains your prior reasoning. Your task is to continue from the current 'Verification' step. I have manually reviewed the reasoning and determined that the **Final Conclusion** is false. Your 'Verification' results must align with mine. Proceed to refine the reasoning by exploring new approaches to solving this problem and construct a new Final Conclusion.

### Output Format
Strictly follow the JSON structure below. All content within the JSON fields must be written in **Chinese**. You do not need to repeat your previous reasoning. Begin directly from the next 'Verification' stage.

```json
{{
"CoT": [
]
}}
```"""

gen_prompt_rethink_Verification = """<question>
{}
</question>

<previous reasoning>
{}
<previous reasoning>

<response requirements>
Your response must include the following steps, each composed of three types of actions: **"Inner Thinking"**, **"Final Conclusion"**, and **"Verification"**:

1. **Inner Thinking**: Break down the reasoning process into multiple concise steps. Each step should start with a brief title to clarify its purpose.
2. **Final Conclusion**: Summarize the correct reasoning from all previous 'Inner Thinking' steps and provide the final answer. No title is needed for this section.
3. **Verification**: Verify the accuracy of the "Final Conclusion". If it holds, conclude the process. Otherwise, return to "Inner Thinking" for further refinement.

</response requirements>

<question> represents the question to be answered, and <previous reasoning> contains your prior reasoning. Your task is to continue from the current 'Verification' step. I have manually reviewed the reasoning and determined that the **Final Conclusion** is false. Your 'Verification' results must align with mine. Proceed to refine the reasoning by conducting a thorough **validation** process to ensure validity and construct a new Final Conclusion.

### Output Format
Strictly follow the JSON structure below. All content within the JSON fields must be written in **Chinese**. You do not need to repeat your previous reasoning. Begin directly from the next 'Verification' stage.

```json
{{
"CoT": [
]
}}
```"""

gen_prompt_rethink_Correction = """<question>
{}
</question>

<previous reasoning>
{}
<previous reasoning>

<response requirements>
Your response must include the following steps, each composed of three types of actions: **"Inner Thinking"**, **"Final Conclusion"**, and **"Verification"**:

1. **Inner Thinking**: Break down the reasoning process into multiple concise steps. Each step should start with a brief title to clarify its purpose.
2. **Final Conclusion**: Summarize the correct reasoning from all previous 'Inner Thinking' steps and provide the final answer. No title is needed for this section.
3. **Verification**: Verify the accuracy of the "Final Conclusion". If it holds, conclude the process. Otherwise, return to "Inner Thinking" for further refinement.

</response requirements>

<question> represents the question to be answered, and <previous reasoning> contains your prior reasoning. Your task is to continue from the current 'Verification' step. I have manually reviewed the reasoning and determined that the **Final Conclusion** is false. Your 'Verification' results must align with mine. Proceed to refine the reasoning by making precise **corrections** to address prior flaws and construct a new Final Conclusion.

### Output Format
Strictly follow the JSON structure below. All content within the JSON fields must be written in **Chinese**. You do not need to repeat your previous reasoning. Begin directly from the next 'Verification' stage.

```json
{{
"CoT": [
]
}}
```"""

gen_prompt_w_label = """<question>
{}
</question>

<previous reasoning>
{}
</previous reasoning>

<response requirements>
Your response must include the following steps, each composed of three types of actions: **"Inner Thinking"**, **"Final Conclusion"**, and **"Verification"**:

1. **Inner Thinking**: Break down the reasoning process into multiple concise steps. Each step should start with a brief title to clarify its purpose.
2. **Final Conclusion**: Summarize the correct reasoning from all previous 'Inner Thinking' steps and provide the final answer. No title is needed for this section.
3. **Verification**: Verify the accuracy of the "Final Conclusion". If it holds, conclude the process. Otherwise, return to "Inner Thinking" for further refinement.

</response requirements>

<question> represents the question to be answered, and <previous reasoning> contains your prior reasoning. Your task is to continue from the current 'Verification' step. Now, I'll secretly tell you that the labeled answer is "{}", but you must pretend not to know. Your 'Verification' requires careful consideration, and if incorrect, you need to provide new Inner Thinking steps and a new Final Conclusion to ensure the final answer aligns with the correct one.

### Output Format
Strictly follow the JSON structure below. All content within the JSON fields must be written in **Chinese**. You do not need to repeat your previous reasoning. Begin directly from the next 'Verification' stage.

```json
{{
"CoT": [
]
}}
```"""

reformat_to_complex_cot_prompt = """<Thought Process>
{}
</Thought Process>

<Question>
{}
</Question>

The <Thought Process> above reflects the model's reasoning based on the <Question>. Your task is to rewrite the <Thought Process> to resemble a more human-like, intuitive natural thinking process in Chinese. The new version should:

1. Be presented as step-by-step reasoning, with each thought on a new line separated by a line break.
2. Avoid structured titles or formatting, focusing on natural transitions. Use casual and natural language for transitions or validations, such as "hmm," "oh," "also," or "wait."
4. Expand the content, making the reasoning richer, more detailed, and logically clear while still being conversational and intuitive.

Return directly the revised natural thinking in JSON format as follows:
```json
{{
}}
```"""

get_final_response_prompt = """<Internal Thinking>
{}
</Internal Thinking>

<Question>
{}
</Question>

The <Internal Thinking> represents your internal thoughts about the <Question>. Based on this, generate a rich and high-quality final response to the user in Chinese. If there is a clear answer, provide it first. Ensure your final response closely follows the <Question>. The response style should resemble GPT-4's style as much as possible. Output only your final response, without any additional content."""

# search strategies
search_strategies = [('Backtracking',gen_prompt_rethink_Backtracking),('Exploring New Paths',gen_prompt_rethink_Exploring_New_Path),('Verification',gen_prompt_rethink_Verification),('Correction',gen_prompt_rethink_Correction)]



def extract_bracket_content(text):
    pass  # TODO: implement

def parse_gpt_response(response):
    pass  # TODO: implement

def parse_gpt_response_reformat(response):
    pass  # TODO: implement


def get_stream_of_search(longcot):
    pass  # TODO: implement

def main():
    pass  # TODO: implement

    def filter_data(tmpdata):
        pass  # TODO: implement








    def verify_gpt(conclusion,answer,d):
        pass  # TODO: implement
    def write_piece_order_data(d):
        pass  # TODO: implement











    def deduplicate_data(data, processed_data):
        pass  # TODO: implement


    def merge_saved_files(save_dir):
        pass  # TODO: implement







if __name__ == '__main__':
