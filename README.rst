Fiducial Registration Educational Demonstration
===============================

.. image:: https://github.com/UCL/FiducialRegistrationEducationalDemonstration/raw/master/project-icon.png
   :height: 128px
   :width: 128px
   :target: https://github.com/UCL/FiducialRegistrationEducationalDemonstration
   :alt: Logo

.. image:: https://github.com/UCL/FiducialRegistrationEducationalDemonstration/badges/master/build.svg
   :target: https://github.com/UCL/FiducialRegistrationEducationalDemonstration/pipelines
   :alt: GitLab-CI test status

.. image:: https://github.com/UCL/FiducialRegistrationEducationalDemonstration/badges/master/coverage.svg
    :target: https://github.com/UCL/FiducialRegistrationEducationalDemonstration/commits/master
    :alt: Test coverage

.. image:: https://readthedocs.org/projects/FiducialRegistrationEducationalDemonstration/badge/?version=latest
    :target: http://FiducialRegistrationEducationalDemonstration.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status



Author: Stephen Thompson

Fiducial Registration Educational Demonstration is part of the `SciKit-Surgery`_ software project, developed at the `Wellcome EPSRC Centre for Interventional and Surgical Sciences`_, part of `University College London (UCL)`_.

Fiducial Registration Educational Demonstration is tested with Python 3.X

Fiducial Registration Educational Demonstration is intended to be used as part of an online tutorial in using fiducial based registration. The tutorial covers the basic theory of fiducial based registration, which is used widely in image guided interventions. The tutorial aims to help the students develop an intuitive understanding of key concepts in fiducial based registration, including Fiducial Localisation Error, Fiducial Registration Error, and Target Registration Error. 

::

    python sksurgery-fred.py

Please explore the project structure, and implement your own functionality.

Developing
----------

Cloning
^^^^^^^

You can clone the repository using the following command:

::

    git clone https://github.com/UCL/scikit-surgeryfred


Running tests
^^^^^^^^^^^^^
Pytest is used for running unit tests:
::

    pip install pytest
    python -m pytest


Linting
^^^^^^^

This code conforms to the PEP8 standard. Pylint can be used to analyse the code:

::

    pip install pylint
    pylint --rcfile=tests/pylintrc sksurgery-fred


Installing
----------

You can pip install directly from the repository as follows:

::

    pip install git+https://github.com/UCL/FiducialRegistrationEducationalDemonstration



Contributing
^^^^^^^^^^^^

Please see the `contributing guidelines`_.


Useful links
^^^^^^^^^^^^

* `Source code repository`_
* `Documentation`_


Licensing and copyright
-----------------------

Copyright 2020 University College London.
Fiducial Registration Educational Demonstration is released under the BSD-3 license. Please see the `license file`_ for details.


Acknowledgements
----------------

Supported by `Wellcome`_ and `EPSRC`_.


.. _`Wellcome EPSRC Centre for Interventional and Surgical Sciences`: http://www.ucl.ac.uk/weiss
.. _`source code repository`: https://github.com/UCL/FiducialRegistrationEducationalDemonstration
.. _`Documentation`: https://FiducialRegistrationEducationalDemonstration.readthedocs.io
.. _`SciKit-Surgery`: https://github.com/UCL/scikit-surgery/wiki
.. _`University College London (UCL)`: http://www.ucl.ac.uk/
.. _`Wellcome`: https://wellcome.ac.uk/
.. _`EPSRC`: https://www.epsrc.ac.uk/
.. _`contributing guidelines`: https://github.com/UCL/FiducialRegistrationEducationalDemonstration/blob/master/CONTRIBUTING.rst
.. _`license file`: https://github.com/UCL/FiducialRegistrationEducationalDemonstration/blob/master/LICENSE

