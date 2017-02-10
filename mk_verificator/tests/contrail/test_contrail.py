

def test_contrail_compute_status(local_salt_client):
    cs = local_salt_client.cmd(
        'cpu*', 'cmd.run', ['contrail-status | grep -Pv \'(==|^$)\'']
    )
    broken_services = []

    for node in cs:
        for line in cs[node].split('\n'):
            line = line.strip()
            name, status = line.split(None, 1)
            if status not in {'active'}:
                err_msg = "{node}:{service} - {status}".format(
                    node=node, service=name, status=status)
                broken_services.append(err_msg)

    assert not broken_services, 'Broken services: {}'.format(broken_services)

def test_contrail_node_status(local_salt_client):
    cs = local_salt_client.cmd(
        'n[tw|al]*', 'cmd.run',
        ['contrail-status | grep -Pv \'(==|^$|Disk|unix|support)\'']
    )
    broken_services = []

    for node in cs:
        for line in cs[node].split('\n'):
            line = line.strip()
            name, status = line.split(None, 1)
            if status not in {'active', 'backup'}:
                err_msg = "{node}:{service} - {status}".format(
                    node=node, service=name, status=status)
                broken_services.append(err_msg)

    assert not broken_services, 'Broken services: {}'.format(broken_services)

def test_contrail_vrouter_count(local_salt_client):
    cs = local_salt_client.cmd(
        'cpu*', 'cmd.run', ['contrail-status | grep -Pv \'(==|^$)\'']
    )

    actual_vrouter_count = 0
    for node in cs:
        for line in cs[node].split('\n'):
            if 'contrail-vrouter-nodemgr' in line:
                actual_vrouter_count += 1

    assert actual_vrouter_count == len(cs.keys()),\
        'The length of vRouters {} differs' \
        ' from the length of compute nodes {}'.format(actual_vrouter_count,
                                                      len(cs.keys()))
