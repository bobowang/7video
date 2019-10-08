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


@cli.command(short_help='fill test records to database')
def fill_test():
    conn = sqlite3.connect(config.DATABASE)
    cur = conn.cursor()
    sql = "insert into forum(cid,tag,url,sn,title,actor,magnet,pics,create_date,create_time)values(?,?,?,?,?,?,?,?,?,?)"
    cur.execute(sql, [
        36,
        u'[无码破解]',
        'https://www.sehuatang.org/thread-178752-1-1.html',
        'ipz-661',
        u'ipz-661  FIRST IMPRESSION 90 某メジャーミスコングランプリ！',
        u'高橋しょう子',
        'magnet:?xt=urn:btih:529842C9F85471478DD21D5B24C1411254382517',
        '''["https://www.assdrty.com/tupian/forum/201909/29/112215kmv2299cllvr2hv9.jpg", "https://jp.netcdn.space/digital/video/ipz00661/ipz00661pl.jpg"]''',
        '2019-09-29', '2019-09-29 11:23:44'])
    conn.commit()
    conn.close()


if __name__ == '__main__':
    cli()
