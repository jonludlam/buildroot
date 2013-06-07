#!/usr/bin/python

# see http://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/RPM_Guide/ch16s04.html

import rpm
import os

ts = rpm.TransactionSet()

spec_dir = 'SPECS'

def specFromFile( spec ):
    return rpm.ts().parseSpec( spec )

spec_names = os.listdir( spec_dir )
specs = {}
for s in spec_names:
    specs[s] = specFromFile( os.path.join( spec_dir, s ) )

# RPM build dependencies.   The 'requires' key for the *source* RPM is
# actually the 'buildrequires' key from the spec
def buildRequiresFromSpec( spec ):
    return spec.sourceHeader['requires']

provides_to_spec = {}
for specname, spec in specs.iteritems():
    for package in spec.packages:
        for provided in (package.header['provides'] + [package.header['name']]):
            provides_to_spec[ provided ] = specname

deps = {}
for specname, spec in specs.iteritems():
    deps[specname]=set()
    for buildreq in buildRequiresFromSpec( spec ):
        # Some buildrequires come from the system repository
        if provides_to_spec.has_key( buildreq ):
            buildreqspec = provides_to_spec[buildreq]
            deps[specname].add(buildreqspec)

def toposort2(data):
    from functools import reduce

    # Ignore self dependencies.
    for k, v in data.items():
        v.discard(k)
    # Find all items that don't depend on anything.
    extra_items_in_deps = reduce(set.union, data.itervalues()) - set(data.iterkeys())
    # Add empty dependences where needed
    extra = {}
    for item in extra_items_in_deps:
	extra[item]=set()
    data.update(extra)
    result = []
    while True:
        ordered = set(item for item, dep in data.iteritems() if not dep)
        if not ordered:
            break
        result.append(ordered)
	newdata = {}
	for item, dep in data.iteritems():
            if item not in ordered:
                newdata[item] = (dep - ordered)
	data = newdata
    assert not data, "Cyclic dependencies exist among these items:\n%s" % '\n'.join(repr(x) for x in data.iteritems())
    return result

result = toposort2(deps)
for x in result:
    for y in x:
        print "rpmbuild -bs < SPECS/%s" % y
        print "mock -r xenserver --resultdir=\"./RPMS/%(target_arch)s/\" SRPMS/* && createrepo RPMS/x86_64"
	print "mv SRPMS/* built_srpms"

