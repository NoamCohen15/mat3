
import re
import shlex
import json

def open_file(path):
    return open(path , encoding="utf-8") 


def process_messages(file):
    datetime = r"^(\d{1,2}\.\d{1,2}\.\d{4}, \d{1,2}:\d{1,2})"
    id = r"([^:]+)"
    text = r"(.*)"
    line_pattern = datetime + " - " + id + ":" + text
    patten = re.compile(line_pattern, re.UNICODE)
    last_dict = dict()
    phone_or_name_dict = dict()
    ctr_phone_or_names_check=1
    list_of_dict=[]
    metadata_lines=[]
    for i in range(3):
        metadata_lines.append(file.readline())
    for line in file:
        #print()
        #print(line)
        m = patten.match(line)
        if m:
            new_dict = {'datetime' : m.group(1) ,
                        'id' : m.group(2) ,
                        'text' : m.group(3)}
            if new_dict['id'] in phone_or_name_dict:
                new_dict['id'] = phone_or_name_dict[m.group(2)]
            else:
                #print("ctr for names", ctr_phone_or_names_check)
                phone_or_name_dict[m.group(2)] = ctr_phone_or_names_check
                #print("phone_or_name_dict[m.group(2)]", phone_or_name_dict[m.group(2)])
                new_dict['id']=phone_or_name_dict[m.group(2)]
                #print("new_dict['id']", new_dict['id'])
                ctr_phone_or_names_check = ctr_phone_or_names_check+1
                #print("ctr new", ctr_phone_or_names_check)
            last_dict = new_dict
            list_of_dict.append(new_dict)
            #print("match")
            #print(f"datetime: {m.group(1)}")
            #print(f"id: {m.group(2)}")
            #print(f"text: {m.group(3)}")
        else:
            #print("not match")
            #print(line)
            if "הוסי" in line:
                continue
            else:
                line = line.rstrip()
                last_dict['text'] = last_dict['text']+line
            
    metadata_dict = dict()
    chat_data= shlex.split(metadata_lines[1])
    phone_pattern = re.compile(r"\+\d{3} \d{2}-\d{3}-\d{4}", re.UNICODE)
    group_creator= re.findall( phone_pattern, metadata_lines[1])
    
    metadata_dict = { 'chat_name' : chat_data[4],
                      'creation_date' : chat_data[0] + " " + chat_data[1],
                      'num_of_participants' : max(phone_or_name_dict.values()),
                      'creator' : group_creator[0] }
    #print(metadata_dict)
    messages_and_matadata_dict = { 'messages' : list_of_dict,
                                   'metadata' : metadata_dict}
    return metadata_dict, messages_and_matadata_dict
    

##main
file = open_file("C:/Users/Noamc/Downloads/�צאט WhatsApp עם יום הולדת בנות לנויה.txt")
metadata_dict, final_dict = process_messages(file)
final_result = open( metadata_dict['chat_name'] +".txt", 'w', encoding= 'utf8')
final_result.write(json.dumps(final_dict, indent = 4, ensure_ascii=False))
final_result.close()