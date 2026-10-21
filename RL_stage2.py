import os
import warnings
from dataclasses import dataclass
import wandb
import torch
from datasets import load_dataset,load_from_disk
from transformers import AutoModelForSequenceClassification, AutoTokenizer,PreTrainedTokenizerBase
import json,random


from trl import (
)

from ppo_utils.ppo_config_medo1 import PPOConfig
from ppo_utils.ppo_trainer_medo1 import PPOTrainer


os.environ["WANDB_MODE"] = "offline"
os.environ['TRANSFORMERS_NO_ADVISORY_WARNINGS'] = 'true'



from transformers import (
)


class ppo_dataset(torch.utils.data.Dataset):
    pass  # TODO: implement
    def __init__(self, data, tokenizer, max_length = 1000,debug = 0):
        pass  # TODO: implement


    def __getitem__(self, index):
        pass  # TODO: implement

    def get_prompt(self,da):
        pass  # TODO: implement



    def collate_fn(self, batch):
        pass  # TODO: implement



    def __len__(self):
        pass  # TODO: implement

if __name__ == "__main__":







