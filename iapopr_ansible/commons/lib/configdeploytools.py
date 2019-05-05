#!/usr/bin/env python
#------coding: utf-8-----------------

import ConfigParser
from lib.deploytools import get_ansible_base_dir, delete_endline, get_deploy_env

class deployconfig:
    def __init__(self):
        self.denv = get_ansible_base_dir()
        self.dconf = ConfigParser.ConfigParser()
        self.cpath = self.denv + '/conf/deploy_python.conf'
        self.dconf.read(self.cpath)
        self.dconf.sections()
    def get_logs_dir(self):
        logdirs = self.dconf.get('deploy_variable', 'logdir')
        logdirs = delete_endline(logdirs)
        return logdirs
    def get_sqlback_dir(self):
        sqldirs = self.dconf.get('deploy_variable', 'backupsql')
        sqldirs = delete_endline(sqldirs)
        return sqldirs
    def get_unpack_dirs(self):
        undirs = self.dconf.get('deploy_variable', 'unpackdir')
        undirs = delete_endline(undirs)
        return undirs
    def get_repos_dirs(self):
        grdirs = self.dconf.get('deploy_variable', 'reposcmd')
        grdirs = delete_endline(grdirs)
        return grdirs
    def get_define_homesize(self):
        hsize = self.dconf.get('deploy_variable', 'homesize')
        return hsize
    def get_define_datasize(self):
        dsize = self.dconf.get('deploy_variable', 'datasize')
        return dsize
    def get_define_memsize(self):
        msize = self.dconf.get('deploy_variable', 'memorysize')
        return msize
    def get_define_backup(self):
        bback = self.dconf.get('deploy_variable', 'backup')
        return bback
    def get_ansible_debug(self):
        gansible = self.dconf.get('ansible', 'ansible_debug')
        return gansible
    def get_backgroup_exec_timeout(self):
        gbet = self.dconf.get('ansible', 'backupground')
        return gbet
    def get_interface_url(self):
        giu = self.dconf.get('deploy_interface', 'host')
        giu = delete_endline(giu)
        return giu
    def get_env_check_interface(self, appcode):
        envc = self.dconf.get('deploy_interface', 'getEnvCheckFlow')
        envc = self.get_interface_url() + envc + '/' + appcode + '/' + get_deploy_env("DEENVID")
        envc = delete_endline(envc)
        return envc
    def post_env_check_interface(self, appcode):
        pbcr = self.dconf.get('deploy_interface', 'getEnvCheckResult')
        pbcr = self.get_interface_url() + pbcr + '/'+ appcode + '/' + get_deploy_env("DEENVID")
        pbcr = delete_endline(pbcr)
        return pbcr
    def get_flowinfo_interface(self, appcode):
        gddi = self.dconf.get('deploy_interface', 'getFlowInfo')
        gddi = self.get_interface_url() + gddi + '/' + appcode
        gddi = delete_endline(gddi)
        return gddi
    def get_startflow_interface(self):
        gsd = self.dconf.get('deploy_interface', 'startFlow')
        gsd = self.get_interface_url() + gsd
        gsd = delete_endline(gsd)
        return gsd
    def check_Jboss_Error(self):
        chJE = self.dconf.get('deploy_log', 'jbossErrorString')
        if chJE.endswith('\''):
            chJE = chJE.rstrip('\'')
        if chJE.startswith('\''):
            chJE = chJE.lstrip('\'')
        if chJE.endswith('\"'):
            chJE = chJE.rstrip('\"')
        if chJE.startswith('\"'):
            chJE = chJE.lstrip('\"')
        if chJE.endswith('|'):
            chJE = chJE.rstrip('|')
        return chJE
    def check_SpringBoot_Erro(self):
        chsbe = self.dconf.get('deploy_log', 'springbootErrorString')
        if chsbe.endswith('\''):
            chsbe = chsbe.rstrip('\'')
        if chsbe.startswith('\''):
            chsbe = chsbe.lstrip('\'')
        if chsbe.endswith('\"'):
            chsbe = chsbe.rstrip('\"')
        if chsbe.startswith('\"'):
            chsbe = chsbe.lstrip('\"')
        return chsbe
    def get_Nginx_Servers(self, appcode):
        getNS = self.dconf.get('deploy_interface', 'getNginxServers')
        getNS = self.get_interface_url() + getNS + '/' + appcode + '/' + get_deploy_env("DEENVID")
        getNS = delete_endline(getNS)
        return getNS
    def post_endflow_interface(self):
        ged = self.dconf.get('deploy_interface', 'endFlow')
        ged = self.get_interface_url() + ged
        ged = delete_endline(ged)
        return ged
    def post_backupfile_list(self):
        pbufl = self.dconf.get('deploy_interface', 'setBackupFileList')
        pbufl = self.get_interface_url() + pbufl
        pbufl = delete_endline(pbufl)
        return pbufl
    def post_setdeployresult_interface(self, taskid):
        gddr = self.dconf.get('deploy_interface', 'setDeployResult')
        gddr = self.get_interface_url() + gddr + '/' + taskid
        gddr = delete_endline(gddr)
        return gddr
    def get_ssu_data_interface(self, appcode):
        gssud = self.dconf.get('deploy_interface', 'getAppData')
        gssud = self.get_interface_url() + gssud + '/' + appcode + '/' + get_deploy_env("DEENVID")
        gssud = delete_endline(gssud)
        return gssud
    def get_db_data_interface(self, appcode):
        gdbdi = self.dconf.get('deploy_interface', 'getDbPwd')
        gdbdi = self.get_interface_url() + gdbdi + '/' + appcode + '/' + get_deploy_env("DEENVID")
        gdbdi = delete_endline(gdbdi)
        return gdbdi
    def get_dilatations_data(self, appcode):
        gdd = self.dconf.get('deploy_interface', 'dilatation')
        gdd = self.get_interface_url() + gdd + '/' + appcode + '/' + get_deploy_env("DEENVID")
        gdd = delete_endline(gdd)
        return gdd
    def get_SetApp_result_interface(self, appcode):
        psrd = self.dconf.get('deploy_interface', 'setAppResult')
        psrd = self.get_interface_url() + psrd + '/' + appcode + '/' + get_deploy_env("DEENVID")
        psrd = delete_endline(psrd)
        return psrd
    def get_setRefreshSoftwareInstResult(self, appcode):
        psrfri = self.dconf.get('deploy_interface', 'setRefreshResult')
        psrfri = self.get_interface_url() + psrfri + '/' + appcode + '/' + get_deploy_env("DEENVID")
        psrfri = delete_endline(psrfri)
        return psrfri
    def get_uninstall_instance_interface(self, appcode):
        puii = self.dconf.get('deploy_interface', 'uninstallInstance')
        puii = self.get_interface_url() + puii + '/' + appcode + '/' + get_deploy_env("DEENVID")
        puii = delete_endline(puii)
        return puii
    def post_instance_result_interface(self):
        piri = self.dconf.get('deploy_interface', 'setSoftwareInstResult')
        piri = self.get_interface_url() + piri + '/' + get_deploy_env("DEENVID")
        piri = delete_endline(piri)
        return piri
    def wget_Japp_configfile_interface(self, appcode):
        gjac = self.dconf.get('deploy_interface', 'javaappconf')
        gjac = self.get_interface_url() + gjac + '/' + appcode + '/' + get_deploy_env("DEENVID")
        gjac = delete_endline(gjac)
        return gjac
