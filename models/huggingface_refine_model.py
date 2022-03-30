
from transformers import T5Config, RobertaTokenizer, T5ForConditionalGeneration
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, RobertaForMaskedLM, pipeline
class huggingface_refine_model:
    def __init__(self,lang):
        self.lang = lang
        self.load_model()

    def load_model(self):
        print("Loading Model")

        self.model = AutoModelForSeq2SeqLM.from_pretrained("mrm8488/codebert2codebert-finetuned-code-refinement")
        self.tokenizer = AutoTokenizer.from_pretrained("mrm8488/codebert2codebert-finetuned-code-refinement")



        print("Loaded Model")

    def predict(self, function_string):
        generator = pipeline('text2text-generation', model=self.model, tokenizer=self.tokenizer)

        output = generator(function_string)[0]


        return output['generated_text']
