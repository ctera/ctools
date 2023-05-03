import logging, time

def fakeFunc(argument):
    logging.info(argument)
    logging.info("Finished single run_cmd task on %s", argument)

    time.sleep(2)
    logging.info("Done")

    return ""