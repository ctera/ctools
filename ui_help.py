from PySide2.QtCore import Qt

from PySide2.QtWidgets import (
    QGridLayout,
    QLineEdit,
    QLabel,
    QCheckBox
)


# Generate the base tool layout
def gen_tool_layout():
    input_widgets = []

    grid = QGridLayout()
    requiredArgs = QLabel("<h4><b>Required Arguments:</b></h4>")
    address = QLabel("Address (Portal IP, hostname, or FQDN):")
    username = QLabel("Portal Admin Username:")
    password = QLabel("Password")
    dev_name = QLabel("Device Name")

    # create input fields
    address_field = QLineEdit()
    username_field = QLineEdit()
    password_field = QLineEdit()
    dev_name_field = QLineEdit()
    
    #add input fields to widgets to be returned
    input_widgets.append(address_field)
    input_widgets.append(username_field)
    input_widgets.append(password_field)
    input_widgets.append(dev_name_field)

    # add widgets to layout
    grid.addWidget(requiredArgs, 0, 0, 1, 2)
    grid.addWidget(address, 1, 0)
    grid.addWidget(username, 1, 1)
    grid.addWidget(address_field, 2, 0)
    grid.addWidget(username_field, 2, 1)
    grid.addWidget(password, 3, 0)
    grid.addWidget(dev_name, 3, 1)
    grid.addWidget(password_field, 4, 0)
    grid.addWidget(dev_name_field, 4, 1)

    return grid, input_widgets

# Generate the base tool layout
def gen_custom_tool_layout(fields, checkboxes, base=True):
    input_widgets = []
    input_labels = {}
    input_fields = {}

    cb_widgets = {}

    grid = QGridLayout()

    requiredArgs = QLabel("<h4><b>Required Arguments:</b></h4>")
    if (base):
        address = QLabel("Address (Portal IP, hostname, or FQDN):")
        username = QLabel("Portal Admin Username:")
        password = QLabel("Password")

        # create input fields
        address_field = QLineEdit()
        username_field = QLineEdit()
        password_field = QLineEdit()

        password_field.setEchoMode(QLineEdit.Password)
    
        #add input fields to widgets to be returned
        input_widgets.append(address_field)
        input_widgets.append(username_field)
        input_widgets.append(password_field)
    
    for index, field in enumerate(fields):
        input_labels[index] = QLabel(field)
        input_fields[index] = QLineEdit()
        input_widgets.append(input_fields[index])

    for index, checkbox in enumerate(checkboxes):
        cb_widgets[index] = QCheckBox(checkbox)
        input_widgets.append(cb_widgets[index])

    # add widgets to layout
    grid.addWidget(requiredArgs, 0, 0, 1, 2)
    
    if (base):
        grid.addWidget(address, 1, 0)
        grid.addWidget(username, 1, 1)
        grid.addWidget(address_field, 2, 0)
        grid.addWidget(username_field, 2, 1)
        grid.addWidget(password, 3, 0)
        grid.addWidget(password_field, 4, 0)

        if (len(fields) + 3) % 2 == 0:
            row_counter = 3
            col_counter = 1
            for i in range(len(fields)):
                grid.addWidget(input_labels[i], row_counter, col_counter)
                grid.addWidget(input_fields[i], row_counter + 1, col_counter)

                if col_counter >= 1:
                    col_counter = 0
                    row_counter += 2
                else: 
                    col_counter += 1
                    
            # Populate the checkboxes into the layout
            for i in range(len(checkboxes)):
                grid.addWidget(cb_widgets[i], row_counter, col_counter)

                if col_counter >= 1:
                    col_counter = 0
                    row_counter += 1
                else:
                    col_counter += 1
        else:
            row_counter = 3
            col_counter = 1

            # Populate the fields into the Grid Layout
            for i in range(len(fields)):
                if i >= len(fields) - 1:
                    if col_counter == 1:
                        grid.addWidget(input_labels[i], row_counter, col_counter)
                        grid.addWidget(input_fields[i], row_counter + 1, col_counter)

                        col_counter = 0
                        row_counter += 2
                    elif col_counter == 0:
                        grid.addWidget(input_labels[i], row_counter, col_counter, 1, 2)
                        grid.addWidget(input_fields[i], row_counter + 1, col_counter, 1, 2)

                        row_counter += 2
                else:
                    grid.addWidget(input_labels[i], row_counter, col_counter)
                    grid.addWidget(input_fields[i], row_counter + 1, col_counter)

                    if col_counter >= 1:
                        col_counter = 0
                        row_counter += 2
                    else: 
                        col_counter += 1

            # Populate the checkboxes into the layout
            for i in range(len(checkboxes)):
                grid.addWidget(cb_widgets[i], row_counter, col_counter)

                if col_counter >= 1:
                    col_counter = 0
                    row_counter += 1
                else:
                    col_counter += 1

    else:
        row_counter = 1
        col_counter = 0
        for i in range(len(fields)):
            if i >= len(fields) - 1:
                if col_counter == 1:
                    grid.addWidget(input_labels[i], row_counter, col_counter)
                    grid.addWidget(input_fields[i], row_counter + 1, col_counter)

                    col_counter = 0
                    row_counter += 2
                elif col_counter == 0:
                    grid.addWidget(input_labels[i], row_counter, col_counter, 1, 2)
                    grid.addWidget(input_fields[i], row_counter + 1, col_counter, 1, 2)

                    row_counter += 2
            else:
                grid.addWidget(input_labels[i], row_counter, col_counter)
                grid.addWidget(input_fields[i], row_counter + 1, col_counter)

                if col_counter >= 1:
                    col_counter = 0
                    row_counter += 2
                else: 
                    col_counter += 1
        # Populate the checkboxes into the layout
        for i in range(len(checkboxes)):
            grid.addWidget(cb_widgets[i], row_counter, col_counter)

            if col_counter >= 1:
                col_counter = 0
                row_counter += 1
            else:
                col_counter += 1
    return grid, input_widgets