from multiprocessing import Queue
from .google.spreadsheetThreadPooler import SpreadsheetThreadPool

# Start SpreadsheetThreadPooler as side process

spreadsheetUpdateQueue = Queue() # Queue used to pass Spreadsheet Update Jobs based off of AttendancePolls
spreadsheetThreadPool = SpreadsheetThreadPool(spreadsheetUpdateQueue)
spreadsheetThreadPool.start()