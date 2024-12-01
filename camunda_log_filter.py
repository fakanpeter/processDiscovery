import re

input_file_path = 'input/gepjarm_try_again.log'
output_file_path = 'CSVs/gepjarmu_try_again.csv'

with open(input_file_path, 'r') as file:
    lines = file.readlines()

extracted_info = []

pattern = r'(\d{4})-(\d{2})-(\d{2}) (\d{2}:\d{2}:\d{2}\.\d{3}).*\n.*intent=ACTIVATE_ELEMENT.*(elementId=(.*?)(?:|$)),.*(processInstanceKey=(.*?)(?:|$)),.*(bpmnProcessId=(.*?)(?:|$)),.*'


extracted_info.append('timestamp;element_id;process_instance_key;bpmn_process_id;\n')
for i in range(len(lines)):
    if "Process process instance event" in lines[i]:
        prev_line = lines[i - 1]
        match = re.search(pattern, lines[i - 1] + lines[i])
        if match:
            yyyy = match.group(1)
            mm = match.group(2)
            dd = match.group(3)
            time = match.group(4)
            element_id = match.group(6)
            bpmn_process_id = match.group(8)
            process_definition_key = match.group(10)
            print(time + "\n")

            if "gateway" not in element_id.lower():
                extracted_info.append(f"{yyyy}.{mm}.{dd} {time};{element_id};{bpmn_process_id};{process_definition_key};\n")


with open(output_file_path, 'w') as output_file:
    output_file.writelines(extracted_info)