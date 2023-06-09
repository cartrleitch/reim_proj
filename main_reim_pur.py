import sqlite3
import sys
import justpy as jp
import pandas as pd
from cosmetic_classes import *

# variables to keep track
# of selected reimbursement or purchase
# across pages
global reim_sel_data
reim_sel_data = ''
global pur_sel_data
pur_sel_data = ''

conn = sqlite3.connect('db_reimbursements.db')

# gets data from query to show employee and reimbursement information
reim_table_data = pd.read_sql_query("SELECT Reimbursements.ReimID, Employee.FirstName AS 'First Name', "
                                    "Employee.LastName AS 'Last Name', "
                                    "Reimbursements.DatePaid, "
                                    "Reimbursements.DateRec AS 'Date Received', Reimbursements.Total FROM Employee "
                                    "INNER JOIN Reimbursements ON "
                                    "Employee.EmpID = Reimbursements.EmpID;", conn)
conn.close()


@jp.SetRoute("/reimbursementtable")
def reim_table():
    # creates webpage and titles it
    wp = jp.WebPage()
    wp.title = 'Reimbursement Table'

    # creates page banner
    banner_div = jp.Div(text='Five Oaks Church', a=wp, classes=banner_classes,
                        style=banner_style,
                        click=banner_click)
    banner_sub = jp.Div(text='Reimbursement Manager', a=banner_div, classes=banner_sub_classes,
                        style='font-size:15px; padding-top: 10px;')

    # divs
    m_table_div = jp.Div(a=wp, classes='flex flex-col items-center py-3')
    r_table_div = jp.Div(a=m_table_div)
    table_div = jp.Div(a=r_table_div, classes='flex flex-row items-center pt-5', style='display:inline-block;')
    table_div2 = jp.Div(a=r_table_div, classes='flex flex-row items-center pt-5', style='display:inline-block;')
    button_div = jp.Div(a=wp, classes='flex flex-col items-center py-3')
    button_div2 = jp.Div(a=button_div, classes='flex flex-row items-center', )
    button_div3 = jp.Div(a=button_div, classes='flex flex-row items-center')
    data_div = jp.Div(a=table_div, style='display:none;')
    data_div2 = jp.Div(a=table_div, style="display:none")

    # table label
    table_label = jp.Div(a=table_div, text='Reimbursement Table', classes=table_title_classes)
    table_label.for_component = table_div

    # takes data from selected reimbursement row
    def reim_selected_row(self, msg):
        if msg.selected:
            self.row_data.text = msg.data
            global reim_sel_data
            reim_sel_data = self.row_data.text
            self.row_selected = msg.rowIndex
            reim_ret()
            ref_sel('', '')
        elif self.row_selected == msg.rowIndex:
            self.row_data.text = ''

    # creates reimbursement table
    grid_reim = reim_table_data.jp.ag_grid(a=table_div,
                                           style="height: 50vh; width: 50vw; max-width: 675px;"
                                                 " margin: 0.25rem; padding: 0.25rem;")
    grid_reim.row_data = data_div
    grid_reim.on('rowSelected', reim_selected_row)
    grid_reim.options.columnDefs[0].hide = True
    grid_reim.options.columnDefs[1].checkboxSelection = True

    conn = sqlite3.connect('db_reimbursements.db')

    # gets data from query to show purchase information
    pur_table_data = pd.read_sql_query("SELECT PurchaseID, PurchaseDate AS 'Purchase Date', Amount, Content, "
                                       "PurchaseType AS 'PurchaseType' FROM Purchase", conn)
    conn.close()

    # takes data from selected purchase row
    def pur_selected_row(self, msg):
        if msg.selected:
            self.row_data.text = msg.data
            global pur_sel_data
            pur_sel_data = self.row_data.text
            self.row_selected = msg.rowIndex
            pur_ret()
        elif self.row_selected == msg.rowIndex:
            self.row_data.text = ''

    # table label
    table_label = jp.Div(a=table_div2, text='Purchases Table', classes=table_title_classes)
    table_label.for_component = table_div2

    # creates purchase table
    grid_pur = pur_table_data.jp.ag_grid(a=table_div2,
                                         style="height: 50vh; width: 40vw; max-width: 575px; "
                                               "margin: 0.25rem; padding: 0.25rem;")
    grid_pur.row_data = data_div2
    grid_pur.on('rowSelected', reim_selected_row)
    grid_pur.options.columnDefs[0].hide = True
    grid_pur.options.columnDefs[1].checkboxSelection = True

    # refreshes data for reimbursement
    # and purchases table
    def refresh_table(self, msg):
        conn = sqlite3.connect('db_reimbursements.db')
        cur = conn.cursor()

        # gets data from query to show employee and reimbursement information
        refreshed_table_data = pd.read_sql_query("SELECT Reimbursements.ReimID, Employee.FirstName AS 'First Name', "
                                                 "Employee.LastName AS 'Last Name', "
                                                 "Reimbursements.DatePaid, "
                                                 "Reimbursements.DateRec AS 'Date Received', Reimbursements.Total FROM "
                                                 "Employee "
                                                 "INNER JOIN Reimbursements ON "
                                                 "Employee.EmpID = Reimbursements.EmpID;", conn)
        # updates displayed reimbursement information
        grid_reim.load_pandas_frame(refreshed_table_data)
        grid_reim.on('rowSelected', reim_selected_row)
        grid_reim.row_data = data_div
        grid_reim.options.columnDefs[0].hide = True
        grid_reim.options.columnDefs[1].checkboxSelection = True

        # gets data from query to show purchase information
        pur_refreshed_table_data = pd.read_sql_query(
            "SELECT PurchaseID, PurchaseDate AS 'Purchase Date', Amount, Content, "
            "PurchaseType AS 'PurchaseType' FROM Purchase", conn)

        # updates displayed purchase information
        grid_pur.load_pandas_frame(pur_refreshed_table_data)
        grid_pur.on('rowSelected', pur_selected_row)
        grid_pur.row_data = data_div
        grid_pur.options.columnDefs[0].hide = True
        grid_pur.options.columnDefs[1].checkboxSelection = True

        conn.commit()
        conn.close()

    # refresh table on page load
    refresh_table('', '')

    # on selection of reimbursement row
    # refresh purchase table to display
    # only purchases belonging to selected
    # reimbursement
    def ref_sel(self, msg):
        conn = sqlite3.connect('db_reimbursements.db')
        cur = conn.cursor()
        reim_val = reim_sel_data['ReimID']
        # updates reimbursement total
        tot = 0
        cur.execute(f'SELECT SUM(Amount) FROM Purchase WHERE ReimID = {reim_val}')
        ret_val = cur.fetchone()
        if ret_val[0] is not None:
            cur.execute(f'SELECT SUM(Amount) FROM Purchase WHERE ReimID = {reim_val}')
            tot_val = cur.fetchone()
            tot = tot_val[0]

        cur.execute(f'UPDATE Reimbursements SET Total = {tot} WHERE ReimID = {reim_val}')

        # gets data from query to show purchase information
        pur_refreshed_table_data = pd.read_sql_query(
            f"SELECT PurchaseID, PurchaseDate AS 'Purchase Date', Amount, Content, "
            f"PurchaseType AS 'PurchaseType' FROM Purchase WHERE ReimID = {reim_val}", conn)

        # updates dispalyed purchase information
        grid_pur.load_pandas_frame(pur_refreshed_table_data)
        grid_pur.on('rowSelected', pur_selected_row)
        grid_pur.row_data = data_div
        grid_pur.options.columnDefs[0].hide = True
        grid_pur.options.columnDefs[1].checkboxSelection = True

        conn.commit()
        conn.close()

    # deletes reimbursement and associated purchases
    def reim_delete_selected(self, msg):
        if reim_sel_data != '':
            conn = sqlite3.connect('db_reimbursements.db')
            cur = conn.cursor()
            reim_del = reim_sel_data['ReimID']
            cur.execute(f"DELETE FROM Reimbursements WHERE ReimID = {reim_del}")
            cur.execute(f"DELETE FROM Purchase WHERE ReimID = {reim_del}")
            conn.commit()
            conn.close()
            refresh_table('', '')

    # deletes purchase
    def pur_delete_selected(self, msg):
        if reim_sel_data != '':
            conn = sqlite3.connect('db_reimbursements.db')
            cur = conn.cursor()
            pur_del = pur_sel_data['PurchaseID']
            reim_val = reim_sel_data['ReimID']
            cur.execute(f"DELETE FROM Purchase WHERE PurchaseID = {pur_del}")
            cur.execute(f'SELECT SUM(Amount) FROM Purchase WHERE ReimID = {reim_val}')
            tot = 0
            ret_val = cur.fetchone()
            if ret_val[0] is not None:
                cur.execute(f'SELECT SUM(Amount) FROM Purchase WHERE ReimID = {reim_val}')
                tot_val = cur.fetchone()
                tot = tot_val[0]

            cur.execute(f'UPDATE Reimbursements SET Total = {tot} WHERE ReimID = {reim_val}')
            conn.commit()
            conn.close()
            refresh_table('', '')

    # marks reimbursement as paid at current date
    def reim_paid(self, msg):
        if reim_sel_data != '':
            conn = sqlite3.connect('db_reimbursements.db')
            cur = conn.cursor()
            reim_val = reim_sel_data['ReimID']
            cur.execute(f"UPDATE Reimbursements SET DatePaid = DATE() WHERE ReimID = {reim_val}")
            conn.commit()
            conn.close()
            refresh_table('', '')

    # button that opens add reimbursement page
    add_reimbursement_button = jp.Button(text='Add Reimb.', type='button', a=button_div2, classes=button_classes,
                                         click=add_reim_red)

    # button that opens employees table page
    employees_button = jp.Button(text='Employees', type='button', a=button_div2, classes=button_classes,
                                 click=employees)

    # button that refreshes table information
    refresh_table_button = jp.Button(text='Refresh', type='button', a=button_div2, classes=button_classes,
                                     click=refresh_table)

    # button that opens edit reimbursement page
    reim_edit_button = jp.Button(text='Edit Reimb.', type='button', a=button_div2,
                                 classes=button_classes, click=reim_edit)

    # button that deletes selected reimbursement
    reim_delete_selected_button = jp.Button(text='Delete Reimb.', type='button', a=button_div2, classes=button_classes,
                                            click=reim_delete_selected)

    # button that opens add purchase page
    add_purchase_button = jp.Button(text='Add Purchase', type='button', a=button_div3, classes=button_classes,
                                    click=add_pur_red)

    # button that deletes selected purchase
    pur_delete_selected_button = jp.Button(text='Delete Purchase', type='button', a=button_div3, classes=button_classes,
                                           click=pur_delete_selected)

    # button that sets reimbursement as paid
    reim_paid_button = jp.Button(text='Mark Paid', type='button', a=button_div3, classes=button_classes,
                                 click=reim_paid)

    # button that opens edit purchase page
    pur_edit_button = jp.Button(text='Edit Purchase', type='button', a=button_div3,
                                classes=button_classes, click=pur_edit)

    return wp


# redirect to add reimbursement page
def add_reim_red(self, msg):
    msg.page.redirect = 'http://127.0.0.1:8000/addreimbursement'


# redirect to edit purchase page
def pur_edit(self, msg):
    if pur_sel_data != '':
        msg.page.redirect = 'http://127.0.0.1:8000/editpurchase'


# redirect to edit reimbursement page
def reim_edit(self, msg):
    if reim_sel_data != '':
        msg.page.redirect = 'http://127.0.0.1:8000/editreimbursement'


# redirect to employee table page
def employees(self, msg):
    msg.page.redirect = 'http://127.0.0.1:8000/employeetable'


# redirect to add purchase page
def add_pur_red(self, msg):
    if reim_sel_data != '':
        msg.page.redirect = 'http://127.0.0.1:8000/addpurchase'


# set reim_id to selected reimbursement's ID
# and return this value when called
def reim_ret():
    reim_id = reim_sel_data['ReimID']
    return reim_id


# set purchase_id to selected purchase's ID
# and return this value when called
def pur_ret():
    pur_id = pur_sel_data['PurchaseID']
    return pur_id
