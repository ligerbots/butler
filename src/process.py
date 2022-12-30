from multiprocessing import Queue
from .processes.spreadsheetBatcher import SpreadsheetBatcher
# from .processes.messenger import Messenger

# Start SpreadsheetThreadPooler as side process
spreadsheetUpdateQueue = Queue() # Queue used to pass Spreadsheet Update Jobs based off of AttendancePolls
spreadsheetThreadPool = SpreadsheetBatcher(spreadsheetUpdateQueue)
spreadsheetThreadPool.start()

