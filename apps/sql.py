#!/usr/bin/env python
# coding=utf-8

import sqlite3

import click

import config

sql_category = '''create table if not exists `category`(
    `id` integer primary key autoincrement,
    `cid` integer unique,
    `title` text
    )
'''

sql_forum = '''create table if not exists `forum`(
    `id` integer primary key autoincrement,
    `cid` integer,      -- 分类ID
    `tag` text,         -- 标签
    `url` text unique,  -- 原帖URL
    `sn` text,          -- 番号
    `title` text,       -- 标题
    `actor` text,       -- 主演
    `magnet` text,      -- 磁力链
    `pics` text,        -- 图片
    `create_date` text, -- 发布日期
    `create_time` text  -- 发布时间
    )
'''


@click.group()
def cli():
    pass


@cli.command(short_help='initialize database and tables')
def init():
    conn = sqlite3.connect(config.DATABASE)
    cur = conn.cursor()
    cur.execute(sql_category)
    cur.execute(sql_forum)
    cur.execute("insert into category(cid,title)values(2, '国产')")
    cur.execute("insert into category(cid,title)values(103, '中文字幕')")
    cur.execute("insert into category(cid,title)values(36, '亚洲无码')")
    cur.execute("insert into category(cid,title)values(37, '亚洲有码')")
    cur.execute("insert into category(cid,title)values(38, '欧美')")
    cur.execute("insert into category(cid,title)values(107, '三级写真')")
    conn.commit()
    conn.close()


if __name__ == '__main__':
    cli()
