import glob,random,re,json,sys
from docx import Document

max_seq_len= 512

def encode_prompt(instructions, inputs):
    input = random.sample(inputs,1)[0]
    instruction = random.sample(instructions,1)[0]
    prompt = {}
    prompt['instruction'] = instruction
    prompt['input'] = input
    return prompt

instructions_para = [
'请以合同审核专家的身份，针对对输入的合同文本的主要内容设计各种问题并给出答案。\
设计问题时需要满足下面要求：\
1.问题的个数不限制。目标是完全了解文本中的内容。\
2.如果文本内容包含有时间、日期、金额，合同基本信息内容，甲乙丙方基本信息内容等重要内容，请设计足够的问题完全覆盖这些内容。\
3.不要问文本中不存在答案的问题。所有问题和答案必须来自该段输入文本内容，不能编造。\
4.示例：问题1：...答案：...问题2：...答案：...'
]

with open('prompts_contract_para.json','w',encoding='utf-8') as res: 
    prompts = []
    result_raw = open('./results_contract_raw.json','r')
    result_raw = json.load(result_raw)
    for result_raw_ in result_raw:
        result = result_raw_['output'].split('段落')
        for duanluo in result:
            if len(duanluo)==0:
                continue
            i = 0
            while duanluo[i].isdigit():
                i+=1
            if duanluo[i] not in ['：',':']:
                #print (duanluo)
                continue
            input = duanluo[i+1:].strip()     
            #print (input)
            if len(input)<30:
                continue 
            #print ('*'*100)
            prompt = encode_prompt(instructions_para, [input])
            prompts.append(prompt)
    
    print (len(prompts))
    json.dump(prompts,res,ensure_ascii=False)
res.close()





