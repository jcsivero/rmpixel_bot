# !pip install openai
# !pip install --upgrade openai
import openai
import os
import json
#openai.api_key = os.getenv("OPENAI_API_KEY")
#openai.Engine.list()


class Gpt3:
        def __init__(self,api_key="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",engine = "text-curie-001",temperature= 0, top_p= 1,max_tokens=512,n = 1):
                self.api_key= api_key
                self.openai= openai
                self.engine = engine
                self.temperature = temperature
                self.top_p = top_p
                self.max_tokens= max_tokens
                self.n = n
                #openai.organization = "RMPixel"                
                openai.api_key= api_key

        
        def list_engine(self):                
                self.engine = openai.Engine.list()["data"]
                return self.engine

        def list_ft(self):
                self.ft =  openai.FineTune.list()["data"]
                return self.ft

        def list_files(self):                 
                self.files= openai.File.list()["data"]
                return self.files

        def delete_all_ft(self):
                self.list_ft()
                for i in self.ft:
                        print (i)                        
                        print(openai.Model.delete(i["fine_tuned_model"]))
                        
        def delete_all_files(self):
                self.list_files()
                for i in self.files:
                        print (i)
                        openai.File.delete(i["id"])
                        

        def prompt(self,text):                         
                response = openai.Completion.create(
                        engine=self.engine,
                        temperature = self.temperature,
                        top_p=self.top_p,                        
                        prompt = text,
                        max_tokens = self.max_tokens,
                        frequency_penalty=1,
                        presence_penalty=1,
                        n=self.n,                        
                )             
                return response["choices"][0]["text"].strip('\n'), response # quito \n iniciales porque aparecen a veces
        
                
        def retrieve_info_file(self, id):
                return openai.File.retrieve(file_id=id)

        def retrieve_info_my_model_ft(self, id):
                return openai.FineTune.retrieve(file_tune_id=id)

        def my_ft_model(self, file_for_train="train.jsonl"):
                self.info_file= openai.File.create(file=open(file_for_train),purpose="fine-tune")                
                self.id_file=self.info_file["id"]

                self.info_model_ft= openai.FineTune.create(training_file=self.id_file)
                

"""             
        def ft_jsonl_create_from_txt(self, path_prompts="./prompts",path_completions="./completions"):
                self.path_prompts= path_prompts
                self.path_completions=path_completions
                files = os.listdir(self.path_prompts)
                print(files)
                data = []

                for f in files:
                        with open(self.path_prompts + f, 'r', encoding='utf-8') as infile:
                                prompts = infile.read()

                        with open(self.path_completions + f, 'r', encoding='utf-8') as infile:
                                completions = infile.read()

                        prompt = '%s\nQUESTIONS:' % context
                        info = {'prompt': prompt, 'completion': questions}
                        data.append(info)


                with open('questions.jsonl', 'w') as outfile:
                        for i in data:
                                json.dump(i, outfile)
                                outfile.write('\n')


"""
