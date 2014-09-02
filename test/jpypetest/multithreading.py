#*****************************************************************************
#   Copyright 2004-2008 Steve Menard
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#	   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#   
#*****************************************************************************
import jpype
import common
import time
import threading
import Queue

class myThread (threading.Thread):
    """
    try to system.println("hello world") and check for exceptions during the call
    
    join() returns False, if any exception during this has been raised.
    """
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.success = False
        self._q = q
        
    def _msg(self, msg):
        print "[" + self.name + "] " + msg

    def run(self):
        self._msg("starting")
        assert jpype.isJVMStarted()
        if not jpype.isThreadAttachedToJVM():
            jpype.attachThreadToJVM()
        else:
            self._msg('already attached')
            print self.name, 
            
        self._msg("trying to access jvm")
        try:
            self._q.put(jpype.java.lang.String(self.name + ": hello world"))
            #time.sleep(1)
            self.success = True
        except:
            self._msg("exception")
            self.success = False
        finally:
            jpype.detachThreadFromJVM()
        
        self._msg("Exiting " + self.name)
        
    def join(self):
        threading.Thread.join(self)
        return self.success

class ThreadingTestCase(common.JPypeTestCase) :
    def setUp(self) :
        # jvm gets started
        common.JPypeTestCase.setUp(self)
    
    def testSequentialThreads(self):
        q = Queue.Queue()
        t1 = myThread(1, "worker-1", q)
        t2 = myThread(2, "worker-2", q)

        t1.start()
        t1.join()
        self.assertEquals(q.get(), t1.name + ": hello world")

        t2.start()
        t2.join()
        self.assertTrue(q.get(), t2.name + ": hello world")

        
    def testParallelThreads(self):
        q = Queue.Queue()
        t1 = myThread(1, "worker-1", q)
        t2 = myThread(2, "worker-2", q)

        t1.start()
        t2.start()

        t1.join()
        t2.join()
        results = q.get(), q.get()
        self.assertItemsEqual(results, [t1.name + ": hello world",
                                        t2.name + ": hello world"])
    
    @classmethod
    def tearDownClass(cls):
        print "tear down"
        jpype.attachThreadToJVM()

