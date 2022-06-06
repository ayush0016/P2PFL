import threading
import logging

from p2pfl.learning.exceptions import ModelNotMatchingError
   
#-----------------------------------------------------------------------
# 
# Revisar otras estrategias de agregación para saber si se adaptarían
#
#-----------------------------------------------------------------------

class Agregator(threading.Thread):

    def __init__(self, n):
        threading.Thread.__init__(self)
        self.node = n
        self.models = {}
        self.lock = threading.Lock()

    def run(self):
        logging.info("Agregating models.")
        self.node.learner.set_parameters(self.agregate(self.models))
        self.clear()
        # Notificamos al nodo
        self.node.on_round_finished()

    def agregate(self,models): print("Not implemented")
            
    def add_model(self, n, m, w):
        # Validar que el modelo sea del mismo tipo

        if self.node.learner.check_parameters(m):
            # Agregar modelo
            self.lock.acquire()
            self.models[n] = ((m, w))
            logging.info("Model added (" + str(len(self.models)) + "/" + str(len(self.node.neightboors)+1) + ")")
            # Check if all models have been added
            if not self.check_and_run_agregation():
                self.lock.release()

        else:
            raise ModelNotMatchingError("Not matching models")
        
    def check_and_run_agregation(self,trhead_safe=False):
        if trhead_safe:
            self.lock.acquire()

        flag = len(self.models)==(len(self.node.neightboors)+1)
        if flag: 
            self.start() 
        
        if trhead_safe:
            self.lock.release()

        return flag

    def clear(self):
        self.__init__(self.node)