from multiprocessing import Process, Pipe, Queue
from .google.sheet_controller import AttendanceSheetController
from .google.spreadsheetThreadPooler import SpreadsheetThreadPooler

# if __name__ == "__main__":
queue = Queue()
# parent_conn, child_conn = Pipe()
spreadsheetThreadPooler = SpreadsheetThreadPooler(queue)
spreadsheetThreadPooler.start()