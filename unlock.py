import menu
from login import login
from filer import get_filer
from cterasdk import *
import logging
from tkinter import messagebox


def unlock(mode, portal, username, password, device_name, tenant_p, Unlock_code):
    global Pro_mode
    Pro_mode = mode
    logging.info('Starting unlock task')
    global_admin = login(mode, portal, username, password)
    filer = get_filer(mode, global_admin, device_name, tenant_p)
    info(filer)
    # passing arguments
    # enable(filer)
    enable(filer, Unlock_code)
    logging.info('Finished unlock task')
    if mode == 'G':
        messagebox.showinfo("Task", 'Finished task. Returning to menu.')
    print('Finished task. Returning to menu.')


def info(filer):
    mac = filer.get('/status/device/MacAddress')
    firmware = filer.get('/status/device/runningFirmware')
    print("Provide the following to CTERA to unlock", filer.name)
    print(mac)
    print(firmware)


def enable(filer, Unlock_code):
    try:
        if Pro_mode == 'G':
            code = Unlock_code
        else:
            code = input("Enter unlock code: ")
    except CTERAException as error:
        logging.warning(error)
        if Pro_mode == 'G':
            messagebox.showerror("Error", "Something went wrong with the prompt.")
        print("Something went wrong with the prompt.")
    try:
        filer.telnet.enable(code)
        if Pro_mode == 'G':
            messagebox.showinfo("Success", "Success. Telnet enabled on" + f'{filer.name}')
        print("Success. Telnet enabled on", filer.name)
    except CTERAException as error:
        logging.warning(error)
        if Pro_mode == 'G':
            messagebox.showerror("Error", "Bad code or something went wrong unlocking device.")
        print("Bad code or something went wrong unlocking device.")


def start_ssh(mode,portal,username,password, E_pubkey):
    logging.info('Starting task to enable SSH on Filer')
    global_admin = login(mode, portal, username, password)
    filer = get_filer(global_admin)
    if mode == 'T':
        pubkey = input("Enter the public key:\n")
    else:
        pubkey=E_pubkey
    cmd = ('exec /config/device startSSHD publicKey "{}"'.format(pubkey))
    filer.cli.run_command(cmd)  # TODO: validate public key
    if mode == 'G':
        messagebox.showinfo("Info:","You may now try to ssh to the Filer:", f'{filer.name}'+'\n'
                            +"If connection is refused, make sure public key is valid.")
    print("You may now try to ssh to the Filer:", filer.name)
    print("If connection is refused, make sure public key is valid.")
    #menu.menu
