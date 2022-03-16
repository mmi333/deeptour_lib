
from transformers import AutoTokenizer, AutoModelForSequenceClassification

import torch
import numpy as np

class huggingface_insecure_code_model:
    def __init__(self):
        self.load_model()

    def load_model(self):
        print("Loading Model")
        self.tokenizer = AutoTokenizer.from_pretrained('mrm8488/codebert-base-finetuned-detect-insecure-code')
        self.model = AutoModelForSequenceClassification.from_pretrained('mrm8488/codebert-base-finetuned-detect-insecure-code')

        print("Loaded Model")

    def predict(self, function_string):
        input_ids = self.tokenizer(function_string, return_tensors="pt").input_ids
        generated_ids = self.model.generate(input_ids, max_length=20)
        description = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        return description
