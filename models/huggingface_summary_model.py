
from transformers import T5Config, RobertaTokenizer, T5ForConditionalGeneration
from transformers import RobertaConfig, RobertaTokenizer, RobertaForMaskedLM, pipeline

class huggingface_summary_model:
    def __init__(self,lang):
        self.lang = lang
        self.load_model()


    def load_model(self):


        print("Loading Model")
        if self.lang in ["py", "js", "java", "cs"]:
            self.tokenizer = RobertaTokenizer.from_pretrained('Salesforce/codet5-base-multi-sum')
            self.model = T5ForConditionalGeneration.from_pretrained('Salesforce/codet5-base-multi-sum')


        print("Loaded Model")

    def predict(self, function_string):
        input_ids = self.tokenizer(function_string, return_tensors="pt").input_ids
        generated_ids = self.model.generate(input_ids)
        description = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        return description
