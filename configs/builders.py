from buildbot.config import BuilderConfig
from buildbot.process.factory import BuildFactory
from buildbot.steps.shell import ShellCommand
from buildbot.steps.shell import TreeSize
from buildbot.steps.source import Git
from buildbot.steps.source import SVN
from buildbot.steps.trigger import Trigger

from slaves import get_slavenames

#######

class MyBuilderConfig(BuilderConfig):
    def __init__(self, name, **kwargs):
        BuilderConfig.__init__(self, name, builddir = "work/builders/" + name, slavenames = get_slavenames(), **kwargs)

# For example see http://buildbot.net/buildbot/docs/0.8.1/reference/buildbot.steps.shell-pysrc.html#Compile
class Maven(ShellCommand):
    name = "mvn"
    haltOnFailure = True
    description = "mvn"

####### BUILDERS

# The 'builders' list defines the Builders, which tell Buildbot how to perform a build:
# what steps, and which slaves can execute them.  Note that any particular build will
# only take place on one slave.

builders = []

# System

system_update_factory = BuildFactory(steps = [
    ShellCommand(command = "sudo -u root cave sync")
])

builders.append(MyBuilderConfig(
    name = "System_Update",
    factory = system_update_factory
))

# JoCoCo

# TODO: IBM JDK, different Maven versions
jacoco_its_factory = BuildFactory(steps = [
    SVN(svnurl = "http://eclemma.svn.sourceforge.net/svnroot/eclemma/jacoco/trunk"),
    Maven(description = "jdk 1.5", command = "mvn -V -e --file org.jacoco.build/pom.xml clean install -Djdk.version=1.5"),
    Maven(description = "jdk 1.6", command = "mvn -V -e --file org.jacoco.build/pom.xml clean install -Djdk.version=1.6"),
    Maven(description = "jdk 1.7", command = "mvn -V -e --file org.jacoco.build/pom.xml clean install -Djdk.version=1.7"),
    TreeSize(),
    Trigger(schedulerNames = ['JaCoCo_Deploy'])
])

# TODO: site at SourceForge
jacoco_deploy_factory = BuildFactory(steps = [
    SVN(svnurl = "http://eclemma.svn.sourceforge.net/svnroot/eclemma/jacoco/trunk"),
    Maven(description = "deploy", command = "mvn -V -e --file org.jacoco.build/pom.xml clean deploy -Djdk.version=1.5"),
    ShellCommand(command = "scp org.jacoco.doc/target/jacoco-*.zip mandrikov,eclemma@web.sourceforge.net:/home/frs/project/e/ec/eclemma/07_JaCoCo/trunk"),
    TreeSize()
])

builders.append(MyBuilderConfig(
    name = "JaCoCo_ITs_Linux",
    factory = jacoco_its_factory
))

builders.append(MyBuilderConfig(
    name = "JaCoCo_Deploy",
    factory = jacoco_deploy_factory
))
