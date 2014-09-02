#*****************************************************************************
#   Copyright 2004-2008 Steve Menard
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#   
#*****************************************************************************

from threading import Thread
from Queue import Queue

import jpype
import common

class ThreadingTestCase(common.JPypeTestCase):

    def _java_printer(self, name, q):
        jpype.attachThreadToJVM()
        q.put(jpype.java.lang.String("foobar %s" % name))
        jpype.detachThreadFromJVM()

    def testParallelThreads(self):
        q = Queue()
        t1 = Thread(target=self._java_printer, args=("thread 1", q))
        t2 = Thread(target=self._java_printer, args=("thread 2", q))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        results = q.get(), q.get()
        self.assertItemsEqual(results, ["foobar thread 1",
                                        "foobar thread 2"])
