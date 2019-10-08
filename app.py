#!/usr/bin/env python
# coding=utf-8

from apps import create_app

if __name__ == '__main__':
    app = create_app()
    app.run()
