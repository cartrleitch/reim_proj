import sqlite3
import sys
import justpy as jp
from cosmetic_classes import *
import time
from main_reim_pur import *


@jp.SetRoute('/editreimbursement')
def edit_reim_main():
    # create and title webpage
    wp = jp.WebPage(delete_flag=False)
    wp.title = 'Add Reimbursement'

    # creates page banner
    banner_div = jp.Div(text='Five Oaks Church', a=wp, classes=banner_classes,
                        style=banner_style,
                        click=banner_click)
    banner_sub = jp.Div(text='Reimbursement Manager', a=banner_div, classes=banner_sub_classes,
                        style='font-size:15px; padding-top: 10px;')
    title_div = jp.Div(text='Reimbursement Add', a=wp,
                       classes=title_classes)
    description_div = jp.Div(text='Create Reimbursement', a=title_div,
                             classes=desc_classes)

    # page divs
    form_div = jp.Div(a=wp, classes='grid h-50')
    form1 = jp.Form(a=form_div, classes='border m-5 p-5 w-100')
    input_div = jp.Div(a=form1, classes='flex flex-col items-center py-1')
    button_div = jp.Div(a=form1, classes='flex flex-col items-center py-3')
    button_div2 = jp.Div(a=button_div, classes='flex flex-row items-center py-3 overflow-hidden')

    # label for employee dropdown menu
    employee_label = jp.Label(a=input_div, text='Employees', classes=label_classes)

    # get employees from database
    conn = sqlite3.connect('db_reimbursements.db')
    cur = conn.cursor()
    cur.execute('SELECT FirstName, LastName, EmpID FROM Employee')
    emp_data = cur.fetchall()
    conn.close()
    emp_data_dict = {}

    # populate dropdown with employee full names
    # store corresponding EmpID in dictionary
    for data in emp_data:
        emp_data_dict[f'{data[0]} {data[1]}'] = data[2]

    select = jp.Select(a=input_div)
    for employee in emp_data_dict:
        select.add(jp.Option(value=employee, text=employee))
    employee_label.for_component = select

    # date entry
    date_label = jp.Label(a=input_div, text='Reimbursement Date', classes=label_classes)
    date_in = jp.Input(a=input_div, placeholder='Date', classes=input_classes, type='date')
    date_label.for_component = date_in

    # button that calls submit_form and puts saved message when pressed
    save_button = jp.Input(value='Save', type='submit', a=button_div2, classes=button_classes,
                           style='cursor: pointer')
    saved_div = jp.Div(text='Saved!', classes='flex flex-row items-center font-bold text-sm text-green-500 invisible',
                       a=button_div)
    saved_div.visibility_state = 'invisible'
    save_button.saved_div = saved_div

    save_button.on('click', show_saved)
    save_button.on('mouseleave', hide_saved)

    # button returns to main page
    done_button = jp.Button(text='Done', type='button', a=button_div2, classes=button_classes,
                            click=done_red)

    # inserts values from entries into table
    def submit_form(self, msg):
        data = msg.form_data
        emp = ''
        date = ''
        for output in data:
            if output['html_tag'] == 'select':
                emp = output.value

            if output['placeholder'] == 'Date':
                date = output.value

        conn = sqlite3.connect('db_reimbursements.db')
        cur = conn.cursor()
        employ = emp_data_dict[emp]
        # updates values for selected reimbursement
        cur.execute('UPDATE Reimbursements SET EmpID = ?, DateRec = ? WHERE ReimID = ?', (employ, date, reim_ret()))

        conn.commit()
        conn.close()

    form1.on('submit', submit_form)

    # creates webpage
    return wp


# redirects to main page
def done_red(self, msg):
    msg.page.redirect = 'http://127.0.0.1:8000/reimbursementtable'


if __name__ == '__main__':
    edit_reim_main()
