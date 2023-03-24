"""Copyright (c) 2019 AIT Lab, ETH Zurich, Xu Chen

Students and holders of copies of this code, accompanying datasets,
and documentation, are not allowed to copy, distribute or modify
any of the mentioned materials beyond the scope and duration of the
Machine Perception course projects.

That is, no partial/full copy nor modification of this code and
accompanying data should be made publicly or privately available to
current/future students or other parties.
"""

from setuptools import setup, find_packages
"""Setup module for project."""

setup(
        name='mp19-project-skeleton',
        version='0.1',
        description='Skeleton code for Machine Perception 3D Pose Estimation project.',

        author='Xu Chen',
        author_email='xuchen@student.ethz.ch',

        packages=find_packages(exclude=[]),
        python_requires='>=3.5',
        install_requires=[
                # Add external libraries here.
                'tensorflow-gpu==2.12.0',
                'numpy',
                'patool',
                'opencv-python',
                'tqdm',
                'h5py',
                'imgaug'
        ],
)
