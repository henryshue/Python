#!/usr/bin/env python
#------coding: utf-8-----------------
import os, subprocess, socket, sys, random, string, commands
import paramiko, json
import tarfile, zipfile

paramiko.util.log_to_file('/data/logs/iapopr/sssh.log', 'INFO')

def deploy_nodes_ping(nodeserver):
    fnull = open(os.devnull, 'w')
    try:
        pingress = subprocess.call('ping', + nodeserver + ' -c 1 -w 1', shell=True, stdout=fnull, stderr=fnull)
        if pingress:
            return False
        else:
            return True
    except Exception as e:
        return e
    finally:
        fnull.close()

def deploy_nodes_port(nodeserver, nodeport):
    deplogsk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    deplogsk.settimeout(10)
    try:
        deplogsk.connect((nodeserver, nodeport))
        return (True, 'Ok')
    except Exception as e:
        return (False, e)
    finally:
        deplogsk.close()

def deploy_nodes_command(nodeserver, nodeport, nodeuser, nodeuserpass, nodecmd):
     deployc = paramiko.SSHClient()
     deployc.set_missing_host_key_policy(paramiko.AutoAddPolicy)
     try:
         deployc.connect(hostname=nodeserver, port=nodeport, username=nodeuser, password=nodeuserpass)
         stdin, stdout, __ = deployc.exec_command(nodecmd)
         stdin.write("Y")
         return stdout.read()
     except Exception as e:
        return e
     finally:
        deployc.close()

def get_deploy_env(name):
    pa = os.getenv(name, None)
    if pa == None:
        print (u"%s Environment variables can not be found"%(name))
        print (u"%.]]$$")
        sys.exit(1)
    else:
        return pa

def delete_endline(endline):
    if endline.endswith('/'):
        endline = endline.rstrip('/')
        return endline
    else:
        return endline

def get_ansible_base_dir():
    path = get_deploy_env('ANSIBLE_BASE_DIR')
    path = delete_endline(path)
    return path

def get_hosts_file_path():
    hostpath = get_ansible_base_dir() + '/hosts/'
    return hostpath

def get_bin_file_path():
    binpath = get_ansible_base_dir() + '/bin/'
    return binpath

def get_apps_file_path():
    appspath = get_ansible_base_dir() + '/apps/'
    return appspath

def get_templates_file_path():
    templates = get_ansible_base_dir() + '/templates/'
    return templates

def get_sbin_file_path():
    sbinpath = get_ansible_base_dir() + '/sbin/'
    return sbinpath

def get_jar_file_path():
    jarpath = get_ansible_base_dir() + '/commons/jar/'
    return jarpath

def delete_file_dir(src):
    safe_made_path = [
        "/data/iapopr/ansible/bin",
        "/data/iapopr/ansible/apps",
        "/data/iapopr/ansible/hosts",
    ]
    for i in safe_made_path:
        if i in src:
            if os.path.isfile(src):
                try:
                    os.remove(src)
                except:
                    pass
            elif os.path.isdir(src):
                for item in os.listdir(src):
                    itemsrc = os.path.join(src, item)
                    delete_file_dir(itemsrc)
                    try:
                        os.rmdir(src)
                    except:
                        pass

def write_host_file(hostdict):
    filename = string.join(random.sample('qwertyuiopasdfghklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM', 10),'')
    try:
        hostfile = file(get_hosts_file_path() + filename, 'w')
        hostfile.write('[devops]\n')
        hostfile.write(hostdict['deployIp'] + ' ansible_ssh_user="' + hostdict['deployUser'] + '"  ansible_ssh_pass="' + hostdict['deployPass'] + '"\n')
    except Exception:
        return None
    finally:
        hostfile.close()

    return filename

def create_inventory_file(hostdict):
    filename = get_hosts_file_path() + string.join(random.sample('qwertyuiopasdfghklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM', 10), '')
    try:
        hostfile = file(filename, 'w')
        hostfile.write('[devops]\n')
        for IP in hostdict["IPs"]:
            hostfile.write(IP + ' ansible_ssh_user="' + hostdict['deployUser'] + '"  ansible_ssh_pass="' + hostdict['deployPass'] + '"\n')
    except Exception:
        return None
    finally:
        hostfile.close()

    return filename

def decrypted_interface_password(encrytioncode):
    #decmd     = 'java -jar ' + get_jar_file_path() + 'szse-cmdb-des.jar ' + '\'' + encrytioncode + '\''
    #edit by hfxu.oth 20190301 加解密采用自己的代码
    decmd    = 'java -jar ' + get_jar_file_path() + 'passwordUtil.jar decode:' + '\'' + encrytioncode + '\''
    resstr    = commands.getoutput(decmd)
    resdic    = json.loads(resstr, 'utf-8')
    #return resdic["data"]
    #新程序加解密统一，并修改了算法
    return resdic

def import_workflow_bpmn(dirPath):
    imwb      = 'java -jar ' + get_jar_file_path() + 'szse-workflow-tool.jar' + dirPath
    imwbres   = commands.getoutput(imwb)
    try:
        imwbDict = json.loads(imwbres, 'utf-8')
        return (True, imwbDict)
    except Exception:
        return (False, imwbres)

def unpack_deploy_package(sfile, dedir):
    if zipfile.is_zipfile(sfile):
        zfs = zipfile.ZipFile(sfile, 'r')
        for zfname in zfs.namelist():
            zfs.extract(zfname, dedir)
        zfs.close()
    elif tarfile.is_tarfile(sfile):
        tfs = tarfile.open(sfile)
        for i in tfs.getnames():
            tfs.extract(i, dedir)
        tfs.close()
    else:
        return None

class deploy_ssh():
    def __init__(self, ip, port, username, password):
        self._ip = ip
        self._port = port
        self._username = username
        self._password = password
    def connect_remote_server(self):
        connTF = False
        try:
            conn = paramiko.Transport((self._ip, self._port))
            conn.connect(username=self._username, password=self._password)
            return conn
        except paramiko.ssh_exception.AuthenticationException,__:
            connTF = False
            return connTF
    def execute_command(self, conns, command):
        rssh = paramiko.SSHClient()
        rssh._transport = conns
        __,stdout, __ = rssh.exec_command(command)
    def get_file(self, conns, rsrc, ldes):
        gsftp = paramiko.SFTPClient.from_transport(conns)
        gsftp.get(rsrc, ldes)
        if os.path.exists(ldes):
            return ldes
        else:
            return False
    def put_file(self, conns, lsrc, rdes):
        psftp = paramiko.SFTPClient.from_transport(conns)
        psftp.put(lsrc, conns)
    def conn_close(self, conns):
        if (conns):
            conns.close()
