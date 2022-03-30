
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, RobertaForMaskedLM, pipeline

class huggingface_java_to_cs_model:
    def __init__(self):
        self.load_model()


    def load_model(self):


        print("Loading Model")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("uclanlp/plbart-java-cs")
        self.tokenizer = AutoTokenizer.from_pretrained("uclanlp/plbart-java-cs")


        print("Loaded Model")

    def predict(self, function_string):
        # input_ids = self.tokenizer(function_string, return_tensors="pt").input_ids
        # generated_ids = self.model.generate(input_ids)
        # description = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        generator = pipeline('text2text-generation', model=self.model, tokenizer=self.tokenizer)
        

        output = generator(function_string, max_length=500)[0]


        return output['generated_text']
