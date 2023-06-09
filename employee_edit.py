import sqlite3
import sys
import justpy as jp
from cosmetic_classes import *
from employee_table import *
import time


@jp.SetRoute('/editemployee')
def edit_emp_main():
    # create and title webpage
    wp = jp.WebPage(delete_flag=False)
    wp.title = 'Add Employee'

    # create page banner
    banner_div = jp.Div(text='Five Oaks Church', a=wp, classes=banner_classes,
                        style=banner_style,
                        click=banner_click)
    banner_sub = jp.Div(text='Reimbursement Manager', a=banner_div, classes=banner_sub_classes,
                        style='font-size:15px; padding-top: 10px;')
    title_div = jp.Div(text='Employee Add', a=wp,
                       classes=title_classes)
    description_div = jp.Div(text='Create Employee', a=title_div,
                             classes=desc_classes)

    # page divs
    form_div = jp.Div(a=wp, classes='grid h-50')
    form1 = jp.Form(a=form_div, classes='border m-5 p-5 w-100')
    input_div = jp.Div(a=form1, classes='flex flex-col items-center py-1')
    button_div = jp.Div(a=form1, classes='flex flex-col items-center py-3')
    button_div2 = jp.Div(a=button_div, classes='flex flex-row items-center py-3')

    # first name entry
    fname_label = jp.Label(a=input_div, text='First Name', classes=label_classes)
    fname_in = jp.Input(a=input_div, placeholder='First Name', classes=input_classes, type='text')
    fname_label.for_component = fname_in

    # last name entry
    lname_label = jp.Label(a=input_div, text='Last Name', classes=label_classes)
    lname_in = jp.Input(a=input_div, placeholder='Last Name', classes=input_classes, type='text')
    lname_label.for_component = lname_in

    # street entry
    street_label = jp.Label(a=input_div, text='Street', classes=label_classes)
    street_in = jp.Input(a=input_div, placeholder='Street', classes=input_classes, type='text')
    street_label.for_component = street_in

    # city entry
    city_label = jp.Label(a=input_div, text='City', classes=label_classes)
    city_in = jp.Input(a=input_div, placeholder='City', classes=input_classes, type='text')
    city_label.for_component = city_in

    # state entry
    state_label = jp.Label(a=input_div, text='State', classes=label_classes)
    state_in = jp.Input(a=input_div, placeholder='State', classes=input_classes, type='text')
    state_label.for_component = state_in

    # zip code entry
    zipcode_label = jp.Label(a=input_div, text='Zip Code', classes=label_classes)
    zipcode_in = jp.Input(a=input_div, placeholder='Zip Code', classes=input_classes, type='text')
    zipcode_label.for_component = zipcode_in

    # job title entry
    jobtitle_label = jp.Label(a=input_div, text='Job Title', classes=label_classes)
    jobtitle_in = jp.Input(a=input_div, placeholder='Job Title', classes=input_classes, type='text')
    jobtitle_label.for_component = jobtitle_in

    # employee account entry
    empaccount_label = jp.Label(a=input_div, text='Employee Account', classes=label_classes)
    empaccount_in = jp.Input(a=input_div, placeholder='Employee Account', classes=input_classes, type='text')
    empaccount_label.for_component = empaccount_in

    # ministry dropdown menu input
    conn = sqlite3.connect('db_reimbursements.db')
    cur = conn.cursor()
    cur.execute('SELECT MinistryID, Desc FROM Ministries')
    min_data = cur.fetchall()
    conn.close()
    min_data_dict = {}
    ministry_label = jp.Label(a=input_div, text='Ministry', classes=label_classes)

    for data in min_data:
        min_data_dict[data[1]] = data[0]
    select = jp.Select(a=input_div)
    for ministry in min_data_dict:
        select.add(jp.Option(value=ministry, text=ministry))
    ministry_label.for_component = select

    # button that calls submit_form when pressed
    save_button = jp.Input(value='Save', type='submit', a=button_div2, classes=button_classes,
                           style='cursor: pointer')
    saved_div = jp.Div(text='Saved!', classes='flex flex-row items-center font-bold text-sm text-green-500 invisible',
                       a=button_div)
    saved_div.visibility_state = 'invisible'
    save_button.saved_div = saved_div

    save_button.on('click', show_saved)
    save_button.on('mouseleave', hide_saved)

    # returns to employee table page
    done_button = jp.Button(text='Done', type='button', a=button_div2, classes=button_classes,
                            click=done_red)

    # inserts values from entries into table
    def submit_form(self, msg):
        data = msg.form_data
        first_name = ''
        last_name = ''
        street = ''
        city = ''
        state = ''
        zip_code = ''
        job_title = ''
        emp_account = ''
        minis = ''

        # assigns variables values from entries
        for output in data:
            if output['placeholder'] == 'First Name':
                first_name = output.value

            if output['placeholder'] == 'Last Name':
                last_name = output.value

            if output['placeholder'] == 'Street':
                street = output.value

            if output['placeholder'] == 'City':
                city = output.value

            if output['placeholder'] == 'State':
                state = output.value

            if output['placeholder'] == 'Zip Code':
                zip_code = output.value

            if output['placeholder'] == 'Job Title':
                job_title = output.value

            if output['placeholder'] == 'Employee Account':
                emp_account = output.value

            if output['html_tag'] == 'select':
                minis = output.value

        conn = sqlite3.connect('db_reimbursements.db')
        cur = conn.cursor()
        emp_val = emp_ret()
        # update selected employee values
        cur.execute('UPDATE Employee SET FirstName = ?, LastName = ?, Street = ?, City = ?, State = ?, ZipCode = ?, '
                    'JobTitle = ?, EmpAccount = ? WHERE EmpID = ?', (first_name, last_name, street, city,
                                                                     state, zip_code, job_title, emp_account, emp_val))
        conn.commit()
        conn.close()
        conn = sqlite3.connect('db_reimbursements.db')
        cur = conn.cursor()
        # update ministry idea for selected employee
        cur.execute("UPDATE EmpMinistry SET MinistryID = ? WHERE EmpID = ?",
                    (min_data_dict[minis], emp_val))
        conn.commit()
        conn.close()

    form1.on('submit', submit_form)

    # creates webpage
    return wp


# redirects to employee table page
def done_red(self, msg):
    msg.page.redirect = 'http://127.0.0.1:8000/employeetable'


if __name__ == '__main__':
    edit_emp_main()
