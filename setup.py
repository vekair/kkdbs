#!/usr/bin/env python
# -*- coding:utf-8 -*-


from setuptools import setup, find_packages

setup(
    name="kkdbs",
    version="0.2.1",
    description=(
        "'mysql','redis','数据库连接池'"
    ),
    long_description="数据库连接池",

    url="https://github.com/vekair/kkdbs.git",
    author="vekair",
    author_email="vekair@126.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["pymysql", "DBUtils==1.3", "logging", "redis"]
)

"""
打包上传
python3 setup.py sdist

twine upload dist/*

python -m pip install kkexcel --upgrade -i https://pypi.org/simple   # 及时的方式，不用等待 阿里云 豆瓣 同步


"""