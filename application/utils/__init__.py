#!/usr/bin/env python  
# coding=utf-8
"""
@author:boris
@Create Time:2020/7/27 00:57
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def table_exists(table_name):
    engine = db.get_engine()
    return engine.dialect.has_table(engine, table_name)


__all__ = ["db", "table_exists"]
