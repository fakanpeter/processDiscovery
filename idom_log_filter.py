import json
import re
import pandas
import pm4py
from datetime import datetime

input_file_path = "input/szigker_foly.detailed.csv"
output_file_path = "models/szigker_foly_detailed_filtered.csv"

def get_deal_id(msg):
    if '"Method name"' not in msg:
        return None
    if '"Return"' not in msg:
        return None
    if ('{"Class":"hu.idomsoft.idcas.kab.rest.controller.startapplication.'
            'StartApplicationUiRestController", "Method name":'
            '"startApplication", "Return"' not in msg):
        return None
    try:
        d = json.loads(msg)
    except json.JSONDecodeError:
        return None
    try:
        return d['Return']
    except KeyError:
        return None

log = pandas.read_csv(input_file_path, sep=',', dtype=str)
deal_ids = log['_source.message'].apply(get_deal_id).dropna().to_numpy().tolist()
print(deal_ids)

deal_id_pattern = "|".join(re.escape(deal_id) for deal_id in deal_ids)
print(deal_id_pattern)
pattern = fr'.*\[([^\]]+)\].*(/api-gateway/[^ ]+/({deal_id_pattern})).*'

filtered_rows = ['timestamp;element_id;process_instance_key;\n']

for index, row in log.iterrows():
    message = row['_source.message']

    match = re.search(pattern, message)
    if match:
        timestamp = match.group(1)
        deal_id = match.group(3)
        uri = match.group(2)

        original_format = '%d/%b/%Y:%H:%M:%S %z'
        desired_format = '%Y.%m.%d %H:%M:%S.%f'
        parsed_datetime = datetime.strptime(timestamp, original_format)
        timestamp = parsed_datetime.strftime(desired_format)[:-3]

        filtered_rows.append(f'{timestamp};{uri.replace(deal_id, '<dealId>')};{deal_id};\n')

with open(output_file_path, 'w') as output_file:
    output_file.writelines(filtered_rows)

output_file.close()

filtered_log = pandas.read_csv(output_file_path, sep=';')
filtered_log = pm4py.format_dataframe(filtered_log, 'process_instance_key', 'element_id',
                                   'timestamp')
process_tree = pm4py.discover_bpmn_inductive(filtered_log)
pm4py.write_bpmn(process_tree, "discovered_model_idom_all_process_v2.bpmn")