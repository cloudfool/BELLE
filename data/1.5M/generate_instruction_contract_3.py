import glob,random,re,json,sys
from docx import Document

def decode_result(input,question,answer):

    assert question.startswith('问题') and answer.startswith('答案')
    id = question.find('：')
    question = question[id+1:]
    id = answer.find('：')
    answer = answer[id+1:]
    result = {}
    result['instruction'] = question
    result['input'] = input
    result['output']  = answer.strip()
    return result


with open('results_contract_train.json','w',encoding='utf-8') as res:
    results = []
    result_raw = open('./results_contract_para.json','r')
    result_raw = json.load(result_raw)
    for result_raw_ in result_raw:
        instruction = result_raw_['instruction']
        output = result_raw_['output']
        input = result_raw_['input']
        if output.startswith('问题1：'):
            output = output.split('\n')
            question_ids = []
            count = 1
            for i,output_ in enumerate(output):
                if output_.startswith( '问题' + str(count)):
                    #print (output_)
                    question_ids.append(i)
                    count += 1
                
            if len(question_ids) == 1:
                next_question_id = question_ids[0]
            for i in range(len(question_ids)-1):
                this_question_id = question_ids[i]
                next_question_id = question_ids[i+1]
                question = output[this_question_id]
                answer = '\n'.join(output[this_question_id+1:next_question_id])
                if len(answer) == 0:
                    print (question)
                    continue

                result = decode_result(input,question,answer)
                
                results.append(result)
                #print (result)
            
            question = output[next_question_id]
            answer = '\n'.join(output[next_question_id+1:])
            if len(answer) > 0:
                result = decode_result(input,question,answer)
                results.append(result)
            else:
                print (question)

    print (len(results))
    json.dump(results,res,indent=2,ensure_ascii=False)
res.close()