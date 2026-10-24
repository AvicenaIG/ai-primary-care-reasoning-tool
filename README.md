# ai-primary-care-reasoning-tool

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Language: Python](https://img.shields.io/badge/Language-Python-3.9-blue.svg)](https://www.python.org/)
[![Version: 0.1.0](https://img.shields.io/badge/Version-0.1.0-blue.svg)](https://github.com/AvicenaIG/ai-primary-care-reasoning-tool)

## Introduction to AI Primary Care Reasoning Tool

The AI Primary Care Reasoning Tool is a medical LLM designed for advanced medical reasoning. It can identify mistakes, explore alternative strategies, and refine its answers.

## Features

### 1. Verifiable Medical Problems

The tool uses verifiable medical problems to guide the search for a complex reasoning trajectory for fine-tuning LLMs.

### 2. Reinforcement Learning

The tool applies reinforcement learning (PPO) with verifier-based rewards to enhance complex reasoning further.

### 3. Advanced Medical Reasoning

The tool can identify mistakes, explore alternative strategies, and refine its answers.

### 4. Medical LLM Fine-Tuning

The tool is designed for fine-tuning LLMs for advanced medical reasoning.

## Installation

```bash
git clone https://github.com/AvicenaIG/ai-primary-care-reasoning-tool.git
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Quick Start

```python
from construct_verifiable_medical_problems import GPT
from SFT_stage1 import Train_dataset
from RL_stage2 import ppo_dataset

# Create a GPT model
gpt = GPT()

# Create a train dataset
train_dataset = Train_dataset()

# Create a PPO dataset
ppo_dataset = ppo_dataset(train_dataset)

# Train the PPO model
ppo_trainer = PPOTrainer()
ppo_trainer.train(ppo_dataset)
```

## Usage

### Example 1: Verifiable Medical Problems

```python
from construct_verifiable_medical_problems import GPT

# Create a GPT model
gpt = GPT()

# Create a verifiable medical problem
verifiable_problem = {"question": "What is the diagnosis of a patient with symptoms of headache and fever?", "answer": "The diagnosis is a viral infection."}

# Use the GPT model to answer the verifiable medical problem
answer = gpt.answer(verifiable_problem)

print(answer)
```

### Example 2: Reinforcement Learning

```python
from SFT_stage1 import Train_dataset
from RL_stage2 import ppo_dataset
from PPOTrainer import PPOTrainer

# Create a train dataset
train_dataset = Train_dataset()

# Create a PPO dataset
ppo_dataset = ppo_dataset(train_dataset)

# Train the PPO model
ppo_trainer = PPOTrainer()
ppo_trainer.train(ppo_dataset)
```

## Configuration

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `PPO_CONFIG_FILE` | str | `~/.ppo_config.json` | Path to the PPO configuration file |
| `VERIFIABLE_MEDICAL_PROBLEMS_FILE` | str | `~/.verifiable_medical_problems.json` | Path to the verifiable medical problems file |

## Contributing

Contributions are welcome! Please create a pull request with a clear description of the changes made.

## License

The AI Primary Care Reasoning Tool is licensed under the MIT license.