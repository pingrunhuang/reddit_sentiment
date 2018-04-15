import os

class MysqlBot:
    sess = None
    tables = []
    username="dev"
    password="dev"
    host="0.0.0.0"
    port="3306"
    database="sentiment"

    info = "mysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(username, password, host, port, database)
    
    def __init__(self):
        self.engine = create_engine(self.info)
        self.sess = Session(bind=self.engine)
        self.tables = self.engine.table_names()
        self.metadata = MetaData()

    def gen_sentiment_table(self):
        if "sentiment" not in self.tables:
            sentiment_table = Table('sentiment', self.metadata,
                Column('id', Integer, autoincrement=True, primary_key=True),
                Column('unix', String(16)),
                Column('title', String(4096)),
                Column('sentiment', String(16)),
                Column('category', String(128)),
                Index("idx_title", "unix"),
            )
            self.metadata.create_all(bind=self.engine)

    def insert(self, table, entries):
        """
        Insert records into tables by batches
        """
        if table not in self.tables:
            self.tables.append(table)
            if table == "sentiment":
                self.gen_sentiment_table()
        self.sess.add_all(entries)
        self.sess.flush()
        self.sess.commit()

    def get_recent_reddit(self, sentiment_term, num=10):
        '''
        rtype: dataframe of the recent reddit
        '''
        if sentiment_term == "":
            query = self.sess.query(Sentiment).filter(Sentiment.category=="all") \
                        .order_by(Sentiment.unix.desc()) \
                        .limit(num)
        else:
            query = self.sess.query(Sentiment).filter(Sentiment.category==sentiment_term) \
                        .order_by(Sentiment.unix.desc()) \
                        .limit(num)
        df = pd.read_sql(query.statement, query.session.bind)
        df["date"] = pd.to_datetime(df["unix"], unit="s")
        df.drop(["id", "unix"], axis=1, inplace=True)
        df = df[["date", "title", "sentiment"]]
        return df
    


database = None
os.environ["isMysql"]="1"

if os.environ.get("isMysql"):
    from sqlalchemy import MetaData, create_engine, Table, MetaData, Column, Index, Integer, String
    from sqlalchemy.orm import Session
    import pandas as pd
    from model import Sentiment

    database = MysqlBot()