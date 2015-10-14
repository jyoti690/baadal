
from gluon import *
import json
# work around to stop stupid editors from complaining about undeclared 'request'
if False:
    request = dict()

def __do(action, vmid):
    #conn = Baadal.Connection("http://10.237.23.178:35357/v2.0", "admin", "admin", "baadal")
    if conn:
        vm = conn.findBaadalVM(id=request.vars.vmid)
        if vm:
            if action == 'start':
                vm.start()
            elif action == 'shutdown':
                vm.shutdown()
            elif action == 'pause':
                vm.pause()
            elif action == 'reboot':
                vm.reboot()
            elif action == 'delete':
                vm.delete()
            elif action == 'resume':
                vm.resume()

        conn.close()
        return jsonify()
    else:
        conn.close()
        return jsonify(status='failure')

def start():
    return __do('start', request.vars.vmid)
    
def shutdown():
    return __do('shutdown', request.vars.vmid)
    
def pause():
    return __do('pause', request.vars.vmid)
    
def reboot():
    return __do('reboot', request.vars.vmid)

def delete():
    return __do('delete', request.vars.vmid)

def resume():
    return __do('resume', request.vars.vmid)


def handle_request():
    action = request.vars.action
    if action == 'approve':
        return __create()
    elif action == 'edit':
        pass
    elif action == 'reject':
        pass
            

def __create():
    #try:
        row = db(db.vm_requests.id == request.vars.id).select()[0]
        #return json.dumps(row)
        vm = conn.createBaadalVM(row.vm_name, row.image, row.flavor, [{'net-id':row.sec_domain}])
        if vm:
            return jsonify()
    #except Exception as e:
        return jsonify(status='fail', message=e.message)

def __reject():
    db(db.vm_requests.id == request.vars.id).delete()
    return jsonify()

def __edit():
    pass