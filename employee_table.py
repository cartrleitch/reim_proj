import sqlite3
import sys
import justpy as jp
import pandas as pd
from cosmetic_classes import *

# variable to keep track of
# selected employee between pages
global emp_sel_data
emp_sel_data = ''

conn = sqlite3.connect('db_reimbursements.db')

# gets data from query to show employee information
emp_table_data = pd.read_sql_query("SELECT EmpID, FirstName, LastName, Street, City, "
                                   "State, ZipCode, JobTitle, EmpAccount FROM Employee", conn)
conn.close()


# takes data from selected row
def selected_row(self, msg):
    if msg.selected:
        self.row_data.text = msg.data
        global emp_sel_data
        emp_sel_data = self.row_data.text
        self.row_selected = msg.rowIndex
        emp_ret()
    elif self.row_selected == msg.rowIndex:
        self.row_data.text = ''


@jp.SetRoute("/employeetable")
def emp_table():
    # creates webpage and titles it
    wp = jp.WebPage()
    wp.title = 'Reimbursement Tables'

    # create page banner
    banner_div = jp.Div(text='Five Oaks Church', a=wp, classes=banner_classes,
                        style=banner_style,
                        click=banner_click)
    banner_sub = jp.Div(text='Reimbursement Manager', a=banner_div, classes=banner_sub_classes,
                        style='font-size:15px; padding-top: 10px;')

    # divs
    table_div = jp.Div(a=wp, classes='flex flex-col items-center pt-5')
    button_div = jp.Div(a=wp, classes='flex flex-col items-center py-3')
    button_div2 = jp.Div(a=button_div, classes='flex flex-row items-center py-3')
    data_div = jp.Div(a=table_div, style='display:none;')

    # table label
    table_label = jp.Div(a=table_div, text='Employee Table', classes=table_title_classes)
    table_label.for_component = table_div

    # creates table
    grid = emp_table_data.jp.ag_grid(a=table_div, style="height: 50vh; width: 60vw; max-width: 1000px; margin: "
                                                        "0.25rem; padding: 0.25rem;")
    grid.on('rowSelected', selected_row)
    grid.row_data = data_div
    grid.options.columnDefs[0].hide = True
    grid.options.columnDefs[1].checkboxSelection = True

    # button that adds employee
    add_employee_button = jp.Button(text='Add', type='button', a=button_div2, classes=button_classes,
                                    click=add_employee)

    # deletes selected employee information
    def delete_selected(self, msg):
        conn = sqlite3.connect('db_reimbursements.db')
        cur = conn.cursor()
        emp_del = emp_sel_data['EmpID']
        cur.execute(f"DELETE FROM Employee WHERE EmpID = {emp_del}")
        cur.execute(f'DELETE FROM Purchase WHERE ReimID IN (SELECT ReimID FROM Reimbursements WHERE EmpID = {emp_del})')
        cur.execute(f'DELETE FROM Reimbursements WHERE EmpID = {emp_del}')
        cur.execute(f'DELETE FROM EmpMinistry WHERE EmpID = {emp_del}')
        conn.commit()
        conn.close()
        refresh_table('', '')

    delete_button = jp.Button(text='Delete', type='button', a=button_div2, classes=button_classes,
                              click=delete_selected)

    # refreshes employee table information
    def refresh_table(self, msg):
        conn = sqlite3.connect('db_reimbursements.db')

        # gets data from query to show employee and reimbursement information
        refreshed_table_data = pd.read_sql_query("SELECT EmpID, FirstName, LastName, Street, City, "
                                                 "State, ZipCode, JobTitle, EmpAccount FROM Employee", conn)
        grid.load_pandas_frame(refreshed_table_data)
        grid.on('rowSelected', selected_row)
        grid.row_data = data_div
        grid.options.columnDefs[0].hide = True
        grid.options.columnDefs[1].checkboxSelection = True

        conn.close()

    # refreshes table on page load
    refresh_table('', '')

    # button for refreshing employee table information
    refresh_table_button = jp.Button(text='Refresh', type='button', a=button_div2, classes=button_classes,
                                     click=refresh_table)

    # button for editing employee values
    edit_employee_button = jp.Button(text='Edit Employee', type='button', a=button_div2, classes=button_classes,
                                     click=edit_employee)

    return wp


# redirects to add employee page
def add_employee(self, msg):
    msg.page.redirect = 'http://127.0.0.1:8000/addemployee'


# redirects to edit employee page
def edit_employee(self, msg):
    msg.page.redirect = 'http://127.0.0.1:8000/editemployee'


# sets emp_id to selected employee
# EmpID and returns emp_id when called
def emp_ret():
    emp_id = emp_sel_data['EmpID']
    return emp_id
