
from transformers import T5Config, RobertaTokenizer, T5ForConditionalGeneration
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, RobertaForMaskedLM, pipeline
class huggingface_refine_model:
    def __init__(self):
        self.load_model()

    def load_model(self):
        print("Loading Model")
        #self.tokenizer = RobertaTokenizer.from_pretrained('Salesforce/codet5-base-multi-sum')
        #self.model = T5ForConditionalGeneration.from_pretrained('Salesforce/codet5-base-multi-sum')

        # self.tokenizer = RobertaTokenizer.from_pretrained('Salesforce/codet5-base')
        # config = T5Config.from_pretrained('Salesforce/codet5-base')
        # self.model_small = T5ForConditionalGeneration.from_pretrained("CodeT5/finetuned_models/refine_small_codet5_base.bin",  config=config)
        # self.model_medium = T5ForConditionalGeneration.from_pretrained("CodeT5/finetuned_models/refine_medium_codet5_base.bin",  config=config)
        #config = RobertaConfig.from_pretrained("mrm8488/codebert2codebert-finetuned-code-refinement-small")

        self.model = AutoModelForSeq2SeqLM.from_pretrained("mrm8488/CodeBERTaPy")
        self.tokenizer = AutoTokenizer.from_pretrained("mrm8488/CodeBERTaPy")



        print("Loaded Model")

    def predict(self, function_string):
        # input_ids = self.tokenizer(function_string, return_tensors="pt").input_ids

        # if input_ids.shape[1] <= 50:
        #   output = self.predict_small(input_ids)
        # elif input_ids.shape[1] <= 100:
        #    output = self.predict_medium(input_ids)
        # else:
        #    output = ""
        generator = pipeline('text2text-generation', model=self.model, tokenizer=self.tokenizer)

        output = generator(function_string)[0]


        return output['generated_text']

    def predict_small(self, input_ids):
        generated_ids = self.model_small.generate(input_ids)
        output = self.tokenizer.decode(generated_ids[0])
        return output

    def predict_medium(self, input_ids):
        generated_ids = self.model_medium.generate(input_ids)
        output = self.tokenizer.decode(generated_ids[0])
        return output

