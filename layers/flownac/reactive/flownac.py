from charmhelpers.core.hookenv import (
    action_get,
    action_fail,
    action_set,
    config,
    status_set,
)

from charms.reactive import (
    remove_state as remove_flag,
    set_state as set_flag,
    when,
)
import charms.sshproxy

cfg = config()


@when('config.changed')
def config_changed():
    if all(k in cfg for k in ['mode']):
        if cfg['mode'] in ['fnc', 'fne', 'fnd', 'fnu']:
            print("Configuring: FlowNAC", cfg['mode'].upper())
    set_flag('flownac.configured')
    status_set('active', 'VNF ready!')
    return

def is_fnc():
    if cfg['mode'] == 'fnc':
        return True
    return False

def is_fne():
    if cfg['mode'] == 'fne':
        return True
    return False

def is_fnd():
    if cfg['mode'] == 'fnd':
        return True
    return False

def is_fnu():
    if cfg['mode'] == 'fnu':
        return True
    return False


@when('flownac.configured')
@when('actions.start')
def start():
    err = ''
    try:
        cmd = "sudo systemctl start flownac.service"
        result, err = charms.sshproxy._run(cmd)
    except:
        action_fail('command failed:' + err)
    else:
        action_set({'stdout': result})
    finally:
        remove_flag('actions.start')
        set_flag('flownac.started')
        status_set('active', 'VNF started!')


@when('flownac.configured')
@when('actions.stop')
def stop():
    err = ''
    try:
        cmd = "sudo systemctl stop flownac.service"
        result, err = charms.sshproxy._run(cmd)
    except:
        action_fail('command failed:' + err)
    else:
        action_set({'stdout': result})
    finally:
        remove_flag('actions.stop')
        remove_flag('flownac.started')
        status_set('active', 'VNF stopped!')


@when('flownac.configured')
@when('actions.restart')
def restart():
    err = ''
    try:
        cmd = "sudo systemctl restart flownac.service"
        result, err = charms.sshproxy._run(cmd)
    except:
        action_fail('command failed:' + err)
    else:
        action_set({'stdout': result})
    finally:
        remove_flag('actions.restart')
        set_flag('flownac.started')
        status_set('active', 'VNF restarted!')

@when('flownac.configured')
@when('actions.check-serv')
def check_serv():
    err = ''
    try:
        #if is_fnu():
        cmd = "./check.sh"
        result, err = charms.sshproxy._run(cmd)
    except:
        action_fail('command failed:' + err)
    else:
        action_set({'stdout': result})
    finally:
        remove_flag('actions.check-serv')

@when('flownac.configured')
@when('actions.start-client')
def start_client():
    err = ''
    try:
        #if is_fnu():
        # Client not prepared for charm execution
        #cmd = "./client.sh"
        cmd = "ls"
        result, err = charms.sshproxy._run(cmd)
    except:
        action_fail('command failed:' + err)
    else:
        action_set({'stdout': result})
    finally:
        remove_flag('actions.start-client')
