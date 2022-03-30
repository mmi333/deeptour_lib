from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

class huggingface_defect_model:
    def __init__(self):
        self.load_model()

    def load_model(self):
        print("Loading Model")

        # self.model = AutoModel.from_pretrained("mrm8488/codebert-base-finetuned-detect-insecure-code")
        # self.tokenizer = AutoTokenizer.from_pretrained("mrm8488/codebert-base-finetuned-detect-insecure-code")
        self.tokenizer = AutoTokenizer.from_pretrained('mrm8488/codebert2codebert-finetuned-code-defect-detection')
        self.model = AutoModelForSequenceClassification.from_pretrained('mrm8488/codebert2codebert-finetuned-code-defect-detection')

        print("Loaded Model")

    def predict(self, function_string):


        # clf = pipeline('text-classification', model=self.model, tokenizer=self.tokenizer)

        # output = clf(function_string)
        # output = output[0]


        # return round(output['score'])
        inputs = self.tokenizer(function_string, return_tensors="pt", truncation=True, padding='max_length')
        labels = torch.tensor([1]).unsqueeze(0)  # Batch size 1
        outputs = self.model(**inputs, labels=labels)
        loss = outputs.loss
        logits = outputs.logits
        return np.argmax(logits.detach().numpy())
