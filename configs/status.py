import sys, os
from buildbot.status import html, mail
from buildbot.status.web import authz

####### STATUS TARGETS

# 'status' is a list of Status Targets. The results of each build will be
# pushed to these targets. buildbot/status/*.py has a variety to choose from,
# including web pages, email senders, and IRC bots.

status = []

authz_cfg=authz.Authz(
    # change any of these to True to enable; see the manual for more options
    gracefulShutdown = False,
    forceBuild = True, # use this to test your slave once it is set up
    forceAllBuilds = False,
    pingBuilder = False,
    stopBuild = False,
    stopAllBuilds = False,
    cancelPendingBuild = False,
)
status.append(html.WebStatus(
    http_port = 8080,
    authz = authz_cfg,
    change_hook_dialects = { 'github' : True }
))


def get_smtp_password():
    path = os.path.join(os.path.dirname(__file__), "passwords/smtp")
    pw = open(path).read().strip()
    return pw

status.append(mail.MailNotifier(
    fromaddr = "robot@godin.net.ru",
    sendToInterestedUsers = False,
    extraRecipients = [ "mandrikov@gmail.com" ],
    useTls = True, relayhost = "smtp.gmail.com", smtpPort = 587,
    smtpUser = "robot@godin.net.ru", smtpPassword = get_smtp_password(),
    mode = "failing",
    builders = ["JaCoCo_ITs_Linux", "JaCoCo_Deploy", "System_Update"]
))
