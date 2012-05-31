'''
Copyright (c) 2012 Sven Reissmann <sven@0x80.io>

This file is part of the PyTgen traffic generator.

PyTgen is free software: you can redistribute it and/or modify it 
under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyTgen is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyTgen. If not, see <http://www.gnu.org/licenses/>.
'''

import logging
import signal

import core.runner
import core.scheduler

from core.generator import *

from config import Conf

def create_jobs():
    logging.getLogger('main').info('Creating jobs')
    
    jobs = []
    for next_job in Conf.jobdef:
        logging.getLogger('main').debug('creating %s', next_job)
        
        job = core.scheduler.job(action = eval(next_job[0])(next_job[2]),
                                 interval = next_job[1][2],
                                 start = next_job[1][0],
                                 end = next_job[1][1])
        jobs.append(job)
        
    return jobs

if __name__ == '__main__':
    logging.basicConfig(level = Conf.loglevel,
                        filename = Conf.logfile)
    
    runner = core.runner(maxthreads = Conf.maxthreads)
    
    jobs = create_jobs()
    
    scheduler = core.scheduler(jobs = jobs, 
                               runner = runner)
    
    # Stop scheduler on exit
    def signal_int(signal, frame):
        logging.getLogger('main').info('Stopping scheduler')
        scheduler.stop()
    
    signal.signal(signal.SIGINT, signal_int)
    
    # Run the scheduler
    logging.getLogger('main').info('Starting scheduler')
    scheduler.start()
    scheduler.join(2 ** 31)
    
    # Stop the runner
    runner.stop()
