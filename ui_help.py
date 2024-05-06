from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QGridLayout,
    QLineEdit,
    QLabel,
    QCheckBox,
    QVBoxLayout,
    QPushButton
)


# Create toolbar given the QStacked Widget and the current selected window
def create_tool_bar(widget, currentWindow):
    tools = QVBoxLayout()

    label = QLabel("<h4><b>Actions:</b></h4>")
    label.setFixedHeight(50)

    run_cmd = QPushButton("Run CMD")
    show_status = QPushButton("Show Status")
    suspend_sync = QPushButton("Suspend Sync")
    unsuspend_sync = QPushButton("Unsuspend Sync")
    enable_ssh = QPushButton("Enable SSH")
    disable_ssh = QPushButton("Disable SSH")
    enable_telnet = QPushButton("Enable Telnet")
    reset_password = QPushButton("Reset Password")
    cloud_folders = QPushButton("CloudFS")
    delete_shares = QPushButton("Delete Shares")
    import_shares = QPushButton("Copy Shares")
    add_members = QPushButton("Add/Remove Members")
    zones_report = QPushButton("Zones Report")

    #STEP8 - Create the push button above so you can navigate to the tool


    # STEP9 - Add the button you just created to the list below. MAKE SURE YOU PUT IT BEFORE EXIT
    tool_list = [run_cmd, show_status, suspend_sync, unsuspend_sync, enable_ssh, disable_ssh, enable_telnet, reset_password, cloud_folders, delete_shares, import_shares, add_members, zones_report]

    tool_list[currentWindow].setStyleSheet("color: darkblue; background-color: lightblue; ")   

    tools.addWidget(label, alignment=Qt.AlignTop)
    
    for tool in tool_list:
        tools.addWidget(tool)

    tools.addStretch()


    #Add button listeners
    for i in range(len(tool_list)):
        if i != currentWindow:
            tool_list[i].clicked.connect(lambda idx=i, i=i: widget.setCurrentIndex(i)) # The idx=i, i=i is a weird type issue with lambdas and the way the listener works
    return tools


# Generate the base tool layout
def gen_tool_layout(toolname):
    input_widgets = []

    grid = QGridLayout()
    tool_header = QLabel("<h2><b>" + str(toolname) + "</b></h2>")
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
    grid.addWidget(tool_header, 0, 0, 1, 2)
    grid.addWidget(requiredArgs, 1, 0, 1, 2)
    grid.addWidget(address, 2, 0)
    grid.addWidget(username, 2, 1)
    grid.addWidget(address_field, 3, 0)
    grid.addWidget(username_field, 3, 1)
    grid.addWidget(password, 4, 0)
    grid.addWidget(dev_name, 4, 1)
    grid.addWidget(password_field, 5, 0)
    grid.addWidget(dev_name_field, 5, 1)

    return grid, input_widgets

# Generate the base tool layout
def gen_custom_tool_layout(toolname, fields, checkboxes, base=True):
    input_widgets = []
    input_labels = {}
    input_fields = {}

    cb_widgets = {}

    grid = QGridLayout()

    tool_header = QLabel("<h2><b>" + str(toolname) + "</b></h2>")
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
    grid.addWidget(tool_header, 0, 0, 1, 2)
    grid.addWidget(requiredArgs, 1, 0, 1, 2)
    
    if (base):
        grid.addWidget(address, 2, 0)
        grid.addWidget(username, 2, 1)
        grid.addWidget(address_field, 3, 0)
        grid.addWidget(username_field, 3, 1)
        grid.addWidget(password, 4, 0)
        grid.addWidget(password_field, 5, 0)

        if (len(fields) + 3) % 2 == 0:
            row_counter = 4
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
            row_counter = 4
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
        row_counter = 2
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