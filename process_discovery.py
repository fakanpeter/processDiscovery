import pandas
import pm4py

compare = True
event_name = 'gepjarmu_try_again'
model_path = "models/discovered_model_100_v2.bpmn"

event_log = pandas.read_csv(f'CSVs/{event_name}.csv', sep=';')
event_log = pm4py.format_dataframe(event_log, 'process_instance_key', 'element_id',
                                   'timestamp')

process_tree = pm4py.discover_bpmn_inductive(event_log)

if compare:


    bpmn_model = pm4py.read_bpmn(model_path)
    net, im, fm = pm4py.convert_to_petri_net(bpmn_model)
    fitness_ali = pm4py.fitness_alignments(event_log, net, im, fm, activity_key='concept:name', case_id_key='case:concept:name', timestamp_key='time:timestamp')
    fitness_tbr = pm4py.fitness_token_based_replay(event_log, net, im, fm, activity_key='concept:name', case_id_key='case:concept:name', timestamp_key='time:timestamp')
    print(f"Fitness: {fitness_ali}")
    print(f"Fitness: {fitness_tbr}")

pm4py.write_bpmn(process_tree, f'models/discovered_model_{event_name}.bpmn')