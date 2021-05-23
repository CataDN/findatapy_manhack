__author__ = 'saeedamen'  # Saeed Amen

#
# Copyright 2016-2020 Cuemacro
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and limitations under the License.
#

# Note you'll need to "pip install s3fs" for this work which is not installed by default by findatapy
# You'll also need to have setup your S3 bucket, and have all your AWS credentials set on your machine
# This article explains how to give S3 rights to other/accounts-users https://stackoverflow.com/questions/45336781/amazon-s3-access-for-other-aws-accounts

# It is recommended NOT to give your S3 access public in general

# NOTE: you need to make sure you have the correct data licences before storing data on disk (and whether other
# users can access it)

from findatapy.market import Market, MarketDataRequest

# In this case we are saving predefined tick tickers to disk, and then reading back
from findatapy.util.dataconstants import DataConstants
from findatapy.market.ioengine import IOEngine

md_request = MarketDataRequest(
    start_date='04 Jan 2021',
    finish_date='05 Jan 2021',
    category='fx',
    data_source='dukascopy',
    freq='tick',
    tickers=['EURUSD'],
    fields=['bid', 'ask', 'bidv', 'askv'],
)

market = Market()

df = market.fetch_market(md_request=md_request)

print(df)

folder = 's3://type_your_s3_bucket here'

# Save to disk in a format friendly for reading later (ie. s3://bla_bla_bla/backtest.fx.tick.dukascopy.NYC.EURUSD.parquet)
# Here it will automatically generate the filename from the folder we gave
# and the MarketDataRequest we made (altenatively, we could have just given the filename directly)
IOEngine().write_time_series_cache_to_disk(folder, df, engine='parquet', md_request=md_request)

md_request.data_engine = folder + '/*.parquet'

df = market.fetch_market(md_request)

print(df)