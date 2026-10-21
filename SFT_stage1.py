import os
import json
import torch
import logging
import argparse

from tqdm import tqdm
import torch.distributed as dist
from torch.utils.data import Dataset, DataLoader
import wandb
from accelerate import Accelerator
from transformers import set_seed, get_cosine_schedule_with_warmup
import shutil
import json
import traceback
from jinja2 import Template

from transformers import AutoModelForCausalLM, AutoTokenizer
os.umask(0)


logger = logging.getLogger(__name__)
logging.basicConfig(level='INFO')


class Train_dataset(torch.utils.data.Dataset):
    pass  # TODO: implement
    def __init__(self, config, tokenizer):
        pass  # TODO: implement



    def __getitem__(self, index):
        pass  # TODO: implement

    def get_response(self,da):
        pass  # TODO: implement


    def get_prompt(self,da):
        pass  # TODO: implement





    def collate_fn(self, batch):
        pass  # TODO: implement

    def __len__(self):
        pass  # TODO: implement

class SFTMetric:
    pass  # TODO: implement
    def __init__(self, device):
        pass  # TODO: implement

    def __call__(self, logits, labels, loss):
        pass  # TODO: implement

    def update(self, logits, labels, loss):
        pass  # TODO: implement

    def get_metric(self, reset=True):
        pass  # TODO: implement




def train(args):
    pass  # TODO: implement













    def save_checkpoint(epoch, step, global_step):
        pass  # TODO: implement













if __name__ == '__main__':







