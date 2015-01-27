import codecs, sys, datetime, logging, os, glob
from filetail import FileTail
from win32com.shell import shell, shellcon

def xcounter(filename):
    log = logging.getLogger(__name__)
    out_hdlr = logging.StreamHandler(sys.stdout)
    out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    out_hdlr.setLevel(logging.INFO)
    log.addHandler(out_hdlr)
    log.setLevel(logging.INFO)

    tail = FileTail(filename)

    count = 0
    time = None
    log.info("Initiated xcounter on %s" % filename)
    for line in tail:
        line = line.rstrip("\r\n")
        if line.count(" -"):
            log.info("Count from %s is %d" % (str(time), count))
            time = datetime.datetime.now()
            count = 0
        elif line.count(" x"):
            count += 1
            log.info(str(count))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        xcounter(sys.argv[1])

    else:
        fleetlogs = {}
        os.chdir(shell.SHGetFolderPath(0, shellcon.CSIDL_PERSONAL, None, 0) + "\EVE\logs\Chatlogs")
        for file in glob.glob("Fleet*"):
            fleetlogs[file] = os.path.getmtime(file)

        maxval = max(fleetlogs, key=fleetlogs.get)
        xcounter(shell.SHGetFolderPath(0, shellcon.CSIDL_PERSONAL, None, 0) + "\EVE\logs\Chatlogs\\" + maxval)