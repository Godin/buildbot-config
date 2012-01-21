from buildbot.schedulers import basic, timed, triggerable

####### SCHEDULERS

# Configure the Schedulers, which decide how to react to incoming changes.

schedulers = []

nightly = timed.Nightly(
    name = "Nightly",
    branch = None,
    builderNames = ["System_Update"],
    minute = 0,
    hour = 1
)
schedulers.append(nightly)

weekly = timed.Nightly(
    name = "Weekly",
    branch = None,
    minute = 0,
    hour = 2,
    dayOfWeek = 7, # 0 = Monday, 7 = Sunday
    builderNames = ["JaCoCo_ITs_Linux"]
)
schedulers.append(weekly)

schedulers.append(basic.SingleBranchScheduler(
    name = "JaCoCo_Checkin",
    branch = None,
    treeStableTimer = 1,
    builderNames = [] # TODO
))

schedulers.append(triggerable.Triggerable(
    name = "JaCoCo_Deploy",
    builderNames = ["JaCoCo_Deploy"]
))
