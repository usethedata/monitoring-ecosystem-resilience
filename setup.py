from setuptools import setup

with open("pyveg/requirements.txt", "r") as f:
    REQUIRED_PACKAGES = f.read().splitlines()


setup(
    name="pyveg",
    version="0.0.1",
    description="Vegetation patterns study.",
    url="https://github.com/alan-turing-institute/monitoring-ecosystem-resilience",
    author="Nick Barlow and Camila Rangel Smith",
    license="MIT",
    include_package_data=True,
    packages=["pyveg",
              "pyveg.src",
              "pyveg.scripts"],
    install_requires=REQUIRED_PACKAGES,
    entry_points={"console_scripts": [
        "pyveg_calc_EC=pyveg.scripts.calc_euler_characteristic:main",
        "pyveg_gen_pattern=pyveg.scripts.generate_pattern:main",
        "pyveg_gee_analysis=pyveg.scripts.analyse_gee_data:main"
    ]

    },
)