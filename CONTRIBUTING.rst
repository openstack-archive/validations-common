If you're interested in contributing to the validations-common project,
the following will help get you started:

   https://docs.openstack.org/infra/manual/developers.html

If you already have a good understanding of how the system works and your
OpenStack accounts are set up, you can skip to the development workflow
section of this documentation to learn how changes to OpenStack should be
submitted for review via the Gerrit tool:

   https://docs.openstack.org/infra/manual/developers.html#development-workflow

Pull requests submitted through GitHub will be ignored.

Validations are meant to verify functionality of tripleo systems.
Therefore a special care should be given to testing your code before submitting a review.

The information below will cover the project specific information you'll
need to get started with validation-framework.

Branches and version management
===============================
Validation Framework project uses semantic versioning and derives names of stable branches
from the released minor versions. The latest minor version released is the only exception
as it is derived from the `master` branch.

Therefore, all code used by version 1.n.* of the project resides in `stable/1.n` branch,
and when version 1.(n+1) is released, new branch `stable/1.(n+1)` will be created.

By default, stable branches recieve only bug fixes and feature backports are decided on case basis
after all the necessary discussions and procedures have taken place.

Documentation
=============
For description of provided validations, modules and tools please refer to the `upstream documentation <https://docs.openstack.org/validations-common/latest/>`_.
Separate documentation is provided about the runtime, `validations-libs <https://docs.openstack.org/validations-libs/latest/>`_

For general information on contributing to OpenStack, please check out the
`contributor guide <https://docs.openstack.org/contributors/>`_ to get started.
It covers all the basics that are common to all OpenStack projects: the accounts
you need, the basics of interacting with our Gerrit review system, how we
communicate as a community, etc.

Communication
=============
* IRC channel ``#validation-framework`` at `Libera`_ (For all subject-matters)
* IRC channel ``#tripleo`` at `OFTC`_ (OpenStack and TripleO discussions)
* Mailing list (prefix subjects with ``[tripleo][validations]`` for faster responses)
  http://lists.openstack.org/cgi-bin/mailman/listinfo/openstack-discuss

.. _Libera: https://libera.chat/
.. _OFTC: https://www.oftc.net/

Contacting the Core Team
========================
Please refer to the `TripleO Core Team
<https://review.opendev.org/#/admin/groups/190,members>`_ contacts.

Bug Tracking
=============
We track our tasks in `Launchpad <https://bugs.launchpad.net/tripleo/+bugs?field.tag=validations>`_ and in
`StoryBoard <https://storyboard.openstack.org/#!/project_group/76>`_

Reporting a Bug
===============
You found an issue and want to make sure we are aware of it? You can do so on
`Launchpad <https://bugs.launchpad.net/tripleo/+filebug>`__. Please, add the
validations tag to your bug.

More info about Launchpad usage can be found on `OpenStack docs page
<https://docs.openstack.org/contributors/common/task-tracking.html#launchpad>`_

Getting Your Patch Merged
=========================
All changes proposed to the TripleO requires two ``Code-Review +2`` votes from
TripleO core reviewers before one of the core reviewers can approve patch by
giving ``Workflow +1`` vote.

Project Team Lead Duties
========================
All common PTL duties are enumerated in the `PTL guide
<https://docs.openstack.org/project-team-guide/ptl.html>`_.

The Release Process for TripleO is documented in `Release Management
<https://docs.openstack.org/tripleo-docs/latest/developer/release.html>`_.

Documentation for the TripleO project can be found `here <https://docs.openstack.org/tripleo-docs/latest/index.html>`_
