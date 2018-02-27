# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import MySQLdb.cursors
class DBPipeline(object):

    def __init__(self):
        self.db_pool = adbapi.ConnectionPool('MySQLdb',
                                             db='capture',
                                             user='root',
                                             passwd='111111',
                                             cursorclass=MySQLdb.cursors.DictCursor,
                                             charset="utf8",
                                             use_unicode=True)

    def process_item(self, item, spider):
        query = self.db_pool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    def _conditional_insert(self, tx, item):
        try:
            sql = 'select * from transfer_records where TxHash = "{TxHash}"'.format(**item)
            tx.execute(sql)
            result = tx.fetchone()
            if result:
                pass
            else:
                sql = 'insert into transfer_records(name,TxHash,Block,From_account,To_account,Value,TxFee,create_time,operate_type) values("{name}","{TxHash}","{Block}","{From_account}","{To_account}",{Value},{TxFee},"{create_time}","{operate_type}")'.format(**item)
                tx.execute(sql)
        except Exception,e:
            print '*'*20
            print sql
            print e

    def handle_error(self, e):
        print 'error',e

