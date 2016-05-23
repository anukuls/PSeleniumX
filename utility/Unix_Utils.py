'''http://stackoverflow.com/questions/3586106/perform-commands-over-ssh-with-python'''

import paramiko
import logging
import Log_Manager

logger = logging.getLogger("utility.Unix_Utils")

def connect(hostname, user, passwd):
    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(hostname, username=user, password=passwd)
    except Exception as e:
        logger.exception("Unable to connect to hostname %s via ssh" % hostname)
        raise
    
    logger.info("Successfully connected to host %s via ssh" % hostname)
    return ssh
    
def executeCommand(ssh, cmd):
    try:
        (stdin, stdout, stderr) = ssh.exec_command(cmd)
    except Exception as e:
        logger.exception("Error executing command %s. Trace : %s" %(cmd, stderr.read()))
        raise
    
    logger.info("Successfully executed command %s" % cmd)
    return stdout.read()
    
def closeConnection(ssh):
    try:
        ssh.close()
    except Exception as e:
        logger.exception("Error closing connection. Trace : %s" % e)
        raise
    
    logger.info("Successfully closed connection")
    
    
# ssh_conn = connect("qevc1.qa1.liveops.com", "root", "Bettr_Passwrd?")
# cmd = "pwd"
# output = executeCommand(ssh_conn, cmd)
# print "output is : ", output
# closeConnection(ssh_conn)

