from buildbot.changes.gitpoller import GitPoller
from buildbot.changes.svnpoller import SVNPoller

####### CHANGESOURCES

sources = []

sources.append(SVNPoller(
    project = "JaCoCo",
    svnurl = "http://eclemma.svn.sourceforge.net/svnroot/eclemma/jacoco/trunk",
    pollinterval = 10 * 60
))
