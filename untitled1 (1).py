# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1knGl9_kBnZk5HkGqMExnJ0bhSf3knM7t
"""

pip install pyspark

#Create Spark Session
from pyspark.sql import SparkSession
spark = SparkSession\
        .builder \
        .appName("Propensitylabs") \
        .getOrCreate()

#Read CSV to Dataframe
data = spark.read\
            .format("csv")\
            .option("header","true")\
            .load("analytics_input.csv")
data.cache()

#Display Schema
data.printSchema()

#Change column names
for i in data.columns:
    n = i.upper()
    data = data.withColumnRenamed(i, n.replace(' ', '_'))

data.printSchema()

from pyspark.sql.functions import col

null_provider_id_rows = data.filter(col("PROVIDER_ID").isNull())
null_provider_id_rows.show()

from pyspark.sql.functions import udf
from pyspark.sql.types import FloatType
convert_to_number = udf(lambda payment_str: float(payment_str.replace('$', '')), FloatType())
# def convert_to_number(payment_str):
    # return float(payment_str.replace('$', ''))

payment_columns = ['_AVERAGE_COVERED_CHARGES_','_AVERAGE_TOTAL_PAYMENTS_', 'AVERAGE_MEDICARE_PAYMENTS']
for col_name in payment_columns:
  data = data.withColumn(col_name, convert_to_number(col_name))
data.show()

data.show()



data_pd = data.toPandas()
data_pd.plot.bar(x="PROVIDER_STATE", y= "_AVERAGE_TOTAL_PAYMENTS_")

data.write.partitionBy('PROVIDER_STATE').parquet("Parquet")

