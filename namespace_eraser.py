from kubernetes import client, config
import os
from pick import pick

config.load_kube_config()
api = client.CoreV1Api()

menu_attr = []
menu_map = {}
idx=0

namespaces = api.list_namespace()

for idx, namespace in enumerate(namespaces.items):
    namespace_name = namespace.metadata.name
    namespace_status = namespace.status.phase
    menu_str = "%-35s : %s" %(namespace_name, namespace_status)
    menu_map[idx] = namespace_name
    menu_attr.append(menu_str)

title = 'Namespace list'

option, index = pick(menu_attr, title, indicator='=>', default_index=0)

selected_ns = f"{menu_map[index]}"

cmd = f'''
kubectl get namespace {selected_ns} -o json \\
  | tr -d "\\n" | sed "s/\\"finalizers\\": \[[^]]\+\]/\\"finalizers\\": []/" \\
  | kubectl replace --raw /api/v1/namespaces/{selected_ns}/finalize -f -
'''

print (cmd)

os.system(cmd)
