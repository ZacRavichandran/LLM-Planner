from setuptools import find_packages, setup

# todo add deps, all that
setup(
    name="llm_planner_alfred",
    packages=find_packages("src"),
    include_package_data=True,
    package_data={"llm_planner_alfred.resources": ["*pkl"]},
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[""],
)
