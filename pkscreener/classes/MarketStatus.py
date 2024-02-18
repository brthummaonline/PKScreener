"""
    The MIT License (MIT)

    Copyright (c) 2023 pkjmesra

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

"""

from PKNSETools.PKNSEStockDataFetcher import nseStockDataFetcher
from PKDevTools.classes.Singleton import SingletonType, SingletonMixin
from PKDevTools.classes.log import default_logger

class MarketStatus(SingletonMixin, metaclass=SingletonType):
    nseFetcher = nseStockDataFetcher()
    def __init__(self):
        super(MarketStatus, self).__init__()

    @property
    def marketStatus(self):
        if "marketStatus" in self.attributes.keys():
            return self.attributes["marketStatus"]
        else:
            self.attributes["lock"] = "" # We don't need threading lock here
            self.marketStatus = ""
            return self.marketStatus
    
    @marketStatus.setter
    def marketStatus(self, status):
        self.attributes["marketStatus"] = status

    def getMarketStatus(self, progress=None, task_id=0):
        lngStatus = ""
        try:
            if progress:
                progress[task_id] = {"progress": 0, "total": 1}
            _,lngStatus,_ = MarketStatus.nseFetcher.capitalMarketStatus()
            if progress:
                progress[task_id] = {"progress": 1, "total": 1}
        except Exception as e:# pragma: no cover
            default_logger().debug(e, exc_info=True)
            pass
        self.marketStatus = lngStatus
        return lngStatus
