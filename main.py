import sqlite3
import sys
import justpy as jp
import pandas as pd
from purchase_add import *
from reimbursement_add import *
from employee_add import *
from main_reim_pur import *
from employee_table import *
from purchase_edit import *
from employee_edit import *
from reimbursement_edit import *
import webbrowser


def main():
    # create webpage (first page is reimbursement table)
    # and open in browser
    webbrowser.open('http://127.0.0.1:8000')
    jp.justpy(reim_table)


if __name__ == '__main__':
    main()
