import multiprocessing


import settings
import time

from engine_v2.getter import Getter
from engine_v2.server import app
from engine_v2.tester import Tester
from utils.log import SimpleLogger


class Engine(object):
    def __init__(self):
        self.logger = SimpleLogger(log_file=settings.ENGINE_LOG_PATH)
        pass
    def run_tester(self,cycle=settings.ENGINE_CYCLE_TESTER):

        if not settings.ENABLE_TESTER:
            self.logger.info("Skipping tester")
            return
        tester = Tester()
        loop =0
        while True :
            self.logger.debug(f"Testing {loop}")
            tester.run()
            loop +=1
            time.sleep(cycle)
    def run_getter(self, cycle=settings.ENGINE_CYCLE_GETTER):
        """
        run getter
        """
        if not settings.ENABLE_GETTER:
            self.logger.info('getter not enabled, exit')
            return
        getter = Getter()
        loop = 0
        while True:
            self.logger.debug(f'getter loop {loop} start...')
            getter.run()
            loop += 1
            time.sleep(cycle)

    def run_server(self):
        if not settings.ENABLE_SERVER:
            self.logger.info('server not enabled, exit')
            return
        app.run(host=settings.SERVER_HOST, port=settings.SERVER_PORT, threaded=settings.SERVER_THREAD,use_reloader=False)

    def run(self):
        global tester_process, getter_process, server_process
        tester_process, getter_process, server_process = None, None, None
        try:
            self.logger.info('starting proxypool...')
            if settings.ENABLE_TESTER:
                tester_process = multiprocessing.Process(
                    target=self.run_tester)
                self.logger.info(f'starting tester, pid {tester_process.pid}...')
                tester_process.start()

            if settings.ENABLE_GETTER:
                getter_process = multiprocessing.Process(
                    target=self.run_getter)
                self.logger.info(f'starting getter, pid {getter_process.pid}...')
                getter_process.start()

            if settings.ENABLE_SERVER:
                server_process = multiprocessing.Process(
                    target=self.run_server)
                self.logger.info(f'starting server, pid {server_process.pid}...')
                server_process.start()

            tester_process and tester_process.join()
            getter_process and getter_process.join()
            server_process and server_process.join()
        except KeyboardInterrupt:
            self.logger.info('received keyboard interrupt signal')
            tester_process and tester_process.terminate()
            getter_process and getter_process.terminate()
            server_process and server_process.terminate()
        finally:
            # must call join method before calling is_alive
            tester_process and tester_process.join()
            getter_process and getter_process.join()
            server_process and server_process.join()
            self.logger.info(
                f'tester is {"alive" if tester_process.is_alive() else "dead"}')
            self.logger.info(
                f'getter is {"alive" if getter_process.is_alive() else "dead"}')
            self.logger.info(
                f'server is {"alive" if server_process.is_alive() else "dead"}')
            self.logger.info('proxy terminated')

if __name__ == '__main__':
    engine = Engine()
    engine.run()
