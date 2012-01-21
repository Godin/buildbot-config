import sys, os
from buildbot.buildslave import BuildSlave

#######

class MySlaveBase(object):
    capabilities = []

    def get_pass(self, name):
        # get the password based on the name
        path = os.path.join(os.path.dirname(__file__), "passwords/%s.slave" % name)
        pw = open(path).read().strip()
        return pw

class MySlave(MySlaveBase, BuildSlave):
    def __init__(self, name, **kwargs):
        password = self.get_pass(name)
        BuildSlave.__init__(self, name, password, **kwargs)

# TODO experimental
def get_slavenames(requirements = []):
    rv = []
    for slave in slaves:
        if set(requirements) > set(slave.capabilities):
            continue
        rv.append(slave.slavename)
    return rv

####### BUILDSLAVES

# 'slavePortnum' defines the TCP port to listen on for connections from slaves.
# This must match the value configured into the buildslaves (with their
# --master option)
slavePortnum = 9989

# The 'slaves' list defines the set of recognized buildslaves. Each element is
# a BuildSlave object, specifying a username and password.  The same username and
# password must be configured on the slave.

slaves = []

slaves.append(MySlave("godin-server"))
slaves.append(MySlave("godin-laptop"))
