import glob,random,re,json,sys
from docx import Document
import utils
import argparse

def main():
    parser = argparse.ArgumentParser(description='chatgpt api')
    parser.add_argument('--input', type=str)
    parser.add_argument('--output', type=str)
    parser.add_argument('--num', type=int)
    args = parser.parse_args()
    args = vars(args)
    args = {k: v for k, v in args.items() if v is not None}
    request_batch_size = 1
    temperature = 1.0
    top_p = 1.0
    #api="completion"
    #model_name="text-davinci-003"
    api="chat"
    model_name="gpt-3.5-turbo"
    Results = []
    with open(args['input']) as fr:
        prompts = json.load(fr)
        for prompt_ in prompts:
            input = prompt_['input']
            instruction = prompt_['instruction']

            input = "<无输入>" if input.lower() == "" else input
            prompt = ''
            prompt += f"指令: {instruction}\n"
            prompt += f"输入:{input}\n"
            prompt += f"输出:"
            batch_inputs = [prompt]
            decoding_args = utils.OpenAIDecodingArguments(
                temperature=temperature,
                n=1,
                max_tokens=1024,  # hard-code to maximize the length. the requests will be automatically adjusted
                top_p=top_p,
                stop=["\n20", "20.", "20."],
            )
        
            results = utils.openai_completion(
                prompts=batch_inputs,
                api=api,
                model_name=model_name,
                batch_size=request_batch_size,
                decoding_args=decoding_args,
                logit_bias={"50256": -100},  # prevent the <|endoftext|> token from being generated
            )
            response = results[0]
            try: #for gpt-3.5-turbo
                raw_instructions = response["message"]["content"]
            except:
                try:
                    raw_instructions = response["text"]  #for text-davinci-003
                except:
                    print("ERROR parse!")
            #print (raw_instructions)
            prompt_['output'] = raw_instructions
            Results.append(prompt_)
            if len(Results)>args['num']:
                break
    with open(args['output'],'w',encoding='utf-8') as res:
        json.dump(Results,res,indent=2,ensure_ascii=False)
    res.close()


if __name__ == '__main__':
    main()
