
from novaclient.exceptions import NotFound
import json,datetime,time
import threading
import Baadal
from utilization import *

@auth.requires_login()
def index():
    return dict()


@auth.requires_login()
def request():
    return dict()


def login():
    return dict()


@auth.requires_login()
def my_vms():
    try:
        conn = Baadal.Connection(_authurl, _tenant, session.username,
                                 session.password)
        vms = conn.baadal_vms()
        response = list()
        for vm in vms:
            vm_properties = vm.properties()
            snapshots = vm.properties()['snapshots']
            for index in range(0, len(snapshots)):
                snapshots[index]['created'] = convert_timezone(
                    snapshots[index]['created'])
            vm_properties['snapshots'] = snapshots
            response.append(vm_properties)
        return jsonify(data=response)
    except Exception as e:
        logger.error(e.message or str(e.__class__))
        return jsonify(status='fail')
    finally:
        try:
            conn.close()
        except NameError:
            pass


@auth.requires_login()
def vm_status():
    try:
        conn = Baadal.Connection(_authurl, _tenant, session.username,
                                 session.password)
        vmid = request.vars.vmid
        vm = conn.find_baadal_vm(id=vmid)
        if vm:
            return jsonify(vm_status=vm.get_status())
    except Exception as e:
        logger.error(e.message() or str(e.__class__))
    finally:
        try:
            conn.close()
        except NameError:
            pass


@auth.requires_login()
def my_requests():
    rows = db(db.vm_requests.requester == session.username).select()
    l = rows.as_list()
    for i in l:
        i['flavor'] = flavor_info(i['flavor'])
        i['sec_domain'] = network_name_from_id(i['sec_domain'])
        i['request_time'] = seconds_to_localtime(i['request_time'])
        i['public_ip_required'] = 'Required' if i['public_ip_required'] == 1 \
            else 'Not Required'
    return jsonify(data=l)


@auth.requires_login()
def my_requests_list():
    return dict()


def register():
    return dict()


###################################GRAPH##############################


#convert graph type from client side into ceilometer type
def get_graph_type(g_type):
    if g_type=="cpu":
        return "cpu_util"
    if g_type=="ram":
        return "memory.usage"
    if g_type=="disk":
        output=[]
        output.append("disk.write.bytes.rate")
        output.append("disk.read.bytes.rate")
        logger.debug(output)
        return output
    if g_type=="nw":
        output=[]
        output.append("network.incoming.bytes.rate")
        output.append("network.outgoing.bytes.rate")
        logger.debug(output)
        return output
    

def get_limit_value(graph_period):
    if graph_period == 'hour':	
        value=12
    elif graph_period == 'day':
        value=12*24
    elif graph_period == 'month':
        value=12*24*30
    elif graph_period == 'week':
        value=12*24*7
    elif graph_period == 'year':
        value=12*24*30*12
    
    return value

  
#fetching graph data from ceilometer 
def fetch_graph_data(vm_info):
    result=[]
    for data in vm_info:
        info={}
        for key,value in data.__dict__.items():
            if key=='volume':
                info['y']=value
            if key=='timestamp':
                str_date=str(value[0:18]).split("T")
                datetime=str_date[0] + " " + str_date[1]
                info['x']=int(time.mktime(time.strptime(datetime, "%Y-%m-%d %H:%M:%S")))*1000
        result.append(info)

    return result


def create_graph():
    ret={}
    vmid=request.vars['vmIdentity']
    graph_period=request.vars['graphPeriod']
    vm_ram=request.vars['vm_RAM']
    g_type=request.vars['graphType']
    m_type=request.vars['mtype']
    result=[]
    logger.error(vmid)
    logger.error(graph_period)
    logger.error(vm_ram)  
    logger.error(g_type)
    gtype=get_graph_type(g_type)
    logger.error(gtype)
    logger.error("welcome")
    limit=get_limit_value(graph_period)
    logger.debug(limit)
    try:
        conn = Baadal.Connection(_authurl, _tenant, session.username,session.password)
        if (g_type=="ram") or (g_type=="cpu"):
            vm_info = conn.fetch_sample_data(vmid,gtype,limit)
           
            graph_data=fetch_graph_data(vm_info)
            
            result=graph_data
           
        if (g_type=="disk") or (g_type=="nw"):
            for graph_type in gtype:
                vm_info = conn.fetch_sample_data(vmid,graph_type,limit)
                graph_data=[]
                graph_data=fetch_graph_data(vm_info)
                result.append(graph_data)
        title=check_graph_type(g_type,vm_ram,m_type)
        host_cpu=request.vars['host_CPU']
        ret['valueformat']=check_graph_period(graph_period)
        ret['y_title']=title['y_title']
        ret['g_title']=title['g_title']
        mem=float(vm_ram)/(1024) if int(vm_ram)>1024 else vm_ram
        ret['data']=result
        ret['mem']=mem
        if g_type=='disk':
            ret['legend_read']='disk read'
            ret['legend_write']='disk write'
        elif g_type=='nw':
            ret['legend_read']='network read'
            ret['legend_write']='network write'
        elif g_type=='cpu':
            ret['name']='cpu'
        else:
            ret['name']='mem'
        json_str = json.dumps(ret,ensure_ascii=False)
	logger.error(json_str)
        return json_str
    except Exception as e:
        logger.exception(e.message() or str(e.__class__))

def show_vm_performance():
    try:
        logger.exception("Entered Performance!!!!!!!!!!!!!")
        logger.exception(session.username)
	logger.exception(session.password)
	logger.exception(_authurl)
	logger.exception(_tenant)
        vmid=request.vars['vmid']
	logger.error(vmid)
        conn = Baadal.Connection(_authurl, _tenant, session.username,session.password)
        logger.exception(conn)
        vm_info = conn.fetch_sample_data(str(vmid),"cpu_util",1)
	logger.exception(vm_info)
        
        for data in vm_info:
            info={}
	    logger.debug(data)
            for key,value in data.__dict__.items():
                if key=='metadata':
                    logger.debug(value)
                    ram=value['flavor.ram']
                    cpu=value['vcpus']
        logger.debug(ram)
	logger.debug(cpu)
	logger.debug(vmid)
        return dict(m_type="vm",vm_ram=ram,vm_cpu=cpu,vm_identity=vmid,vm_id = vmid)
    except Exception as e:
        logger.exception(e.message() or str(e.__class__))
    
    finally:
        try:
            conn.close()
        except NameError:
            pass
