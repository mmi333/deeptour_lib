
from transformers import T5Config, RobertaTokenizer, T5ForConditionalGeneration
from transformers import BertForSequenceClassification, AutoTokenizer, RobertaForMaskedLM, pipeline

class huggingface_defect_model:
    def __init__(self):
        self.load_model()

    def load_model(self):
        print("Loading Model")

        self.model = BertForSequenceClassification.from_pretrained("mrm8488/codebert2codebert-finetuned-code-defect-detection")
        self.tokenizer = AutoTokenizer.from_pretrained("mrm8488/codebert2codebert-finetuned-code-defect-detection")

        print("Loaded Model")

    def predict(self, function_string):
        # input_ids = self.tokenizer(function_string, return_tensors="pt").input_ids
        # generated_ids = self.model.generate(input_ids, max_length=20)
        # description = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)


        clf = pipeline('text-classification', model=self.model, tokenizer=self.tokenizer)

        output = clf(function_string)
        output = output[0]


        return str(output['score'])