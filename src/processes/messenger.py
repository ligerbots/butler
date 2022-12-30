# from multiprocessing import Process
# from app import app

# # Send slack messages to users when it is time for a meeting based off of the spreadsheet
# class Messenger(Process):
#     def __init__(self, messageQueue, logger):
#         super().__init__()
#         self.messageQueue = messageQueue
#         self.logger = logger
#         self.app = app

#     def run(self):
#         self.logger.info("Messenger Process Started")
#         while True:
           