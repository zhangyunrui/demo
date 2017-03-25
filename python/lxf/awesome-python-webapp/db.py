# coding:utf8
import logging
import threading

# global engine object
import time

engine = None


def _profiling(start, sql=''):
    """
    解析sql执行的时间
    :param start:
    :param sql:
    :return:
    """
    t = time.time() - start
    if t > 0.1:
        logging.warning('[PROFILING][DB] %s: %s' % (t, sql))
    else:
        logging.warning('[PROFILING][DB] %s: %s' % (t, sql))


def create_engine(user, password, database, host='127.0.0.1', port=3306, **kw):
    """
    db模型的核心函数，用于连接数据库，生成全局的engine
    engine对象持有数据库连接
    :param user:
    :param password:
    :param database:
    :param host:
    :param port:
    :param kw:
    :return:
    """
    import mysql.connector
    global engine
    if engine is not None:
        raise DBError('Engine is already initialized.')
    params = dict(user=user, password=password, database=database, host=host, port=port)
    defaults = dict(use_unicode=True, charset='utf8', collation='utf8_general_ci', autocommit=False)
    for k, v in defaults.iteritems():
        params[k] = kw.pop(k, v)
    params.update(kw)
    params['buffered'] = True
    engine = _Engine(lambda: mysql.connector.Connect(**params))
    logging.info('init mysql engine <%s> ok.' % hex(id(engine)))


# def connection():
#     return _ConnectionCtx()


def with_connection(func):
    def _wrapper(*args, **kw):
        with _ConnectionCtx():
            return func(*args, **kw)

    return _wrapper


# def transaction():
#     return _TransactionCtx()


def with_transaction(func):
    def _wrapper(*args, **kw):
        start = time.time()
        with _TransactionCtx():
            return func(*args, **kw)
        _profiling(start)

    return _wrapper


@with_connection
def _update(sql, *args):
    """
    执行update语句，返回update行数
    :param sql:
    :param args:
    :return:
    """
    global _db_ctx
    cursor = None
    sql = sql.replace('?', '%s')
    logging.info('SQL: %s, ARGS: %s' % (sql, args))
    try:
        cursor = _db_ctx.connection.cursor()
        cursor.execute(sql, args)
        r = cursor.rowcount
        if _db_ctx.transactions == 0:
            logging.info('auto commit')
            _db_ctx.connection.commit()
        return r
    finally:
        if cursor:
            cursor.close()


def update(sql, *args):
    return _update(sql, *args)


class DBError(Exception):
    pass


class MultiColumnsError(DBError):
    pass


# 数据库引擎对象
class _Engine(object):
    def __init__(self, connect):
        self._connect = connect

    def connect(self):
        return self._connect()


class _LasyConnection(object):
    """
    惰性连接对象
    仅当需要cursor对象时，才连接数据库，获取连接
    """

    def __init__(self):
        self.connection = None

    def cursor(self):
        if self.connection is None:
            _connection = engine.connect()
            logging.info('[CONNECTION] [OPEN] connection <%s>...' % hex(id(_connection)))
            self.connection = _connection
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def cleanup(self):
        if self.connection:
            _connection = self.connection
            self.connection = None
            logging.info('[CONNECTION] [CLOSE] connection <%s>...' % hex(id(_connection)))
            _connection.close()


# 持有数据库连接的上下文对象
class _Dbctx(threading.local):
    """
    db模块的核心对象，数据库连接的上下文对象，负责从数据库获取和释放连接
    取得的连接是惰性连接对象，因此只有调用cursor对象时，才会真正获取数据库连接
    该对象是一个 Thread local对象，因此绑定在此对象上的数据仅对本线程可见
    """

    def __init__(self):
        self.connection = None
        self.transactions = 0

    def is_init(self):
        return not self.connection is None

    def init(self):
        self.connection = _LasyConnection()
        self.transactions = 0

    def cleanup(self):
        self.connection.cleanup()
        self.connection = None

    def cursor(self):
        return self.connection.cursor()


_db_ctx = _Dbctx()


class _ConnectionCtx(object):
    """
    实现连接的自动获取和释放
    """

    def __enter__(self):
        global _db_ctx
        self.should_cleanup = False
        if not _db_ctx.is_init():
            _db_ctx.init()
            self.should_cleanup = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        global _db_ctx
        if self.should_cleanup:
            _db_ctx.cleanup()


class _TransactionCtx(object):
    """
    每遇到一层嵌套就+1,离开一层嵌套就-1,最后到0时提交事务
    """

    def __enter__(self):
        global _db_ctx
        self.should_close_conn = False
        if not _db_ctx.is_init():
            # need to open a connection firstly
            _db_ctx.init()
            self.should_close_conn = True
        _db_ctx.transactions += 1
        logging.info('begin transaction...' if _db_ctx.transactions == 1 else 'join current transaction.')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        global _db_ctx
        _db_ctx.transactions -= 1
        try:
            if _db_ctx.transactions == 0:
                if exc_type is None:
                    self.commit()
                else:
                    self.rollback()
        finally:
            if self.should_close_conn:
                _db_ctx.cleanup()

    def commit(self):
        global _db_ctx
        logging.info('commit transaction...')
        try:
            _db_ctx.connection.commit()
            logging.info('commit ok.')
        except:
            logging.warning('commit failed. try rollback...')
            _db_ctx.connection.rolback()
            logging.warning('rollback ok.')
            raise

    def rollback(self):
        global _db_ctx
        logging.warning('rollback transation...')
        _db_ctx.connection.rolback()
        logging.info('rollback ok.')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    create_engine('root', '1234', 'test1')
    time.sleep(3)
    update('update test1 set ti = %s;', 100)
