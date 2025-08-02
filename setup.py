from setuptools import setup, find_packages

setup(
    name="p2pshare",
    version="0.1",
    description="Send and receive files between PC and phone using a local webserver + QR code.",
    author="Zhuosiwaaa",
    author_email="joshuablazer@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "qrcode",
        "werkzeug",
        'waitress',
    ],
    entry_points={
        'console_scripts': [
            'p2pshare = p2pshare.main:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
