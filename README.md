### logformat

```
import logformat

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename='/tmp/xxxx.log',
    filemode='w',
)

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)

formatter = logformat.ColorFormater('%(levelname)-8s %(message)s')
console.setFormatter(formatter)

logging.getLogger('').addHandler(console)



logging.debug("debug")
logging.info("info")
logging.warning("warning")
logging.critical("critical")
logging.error("error")

```

![本来是效果图](http://1-im.guokr.com/Wa3clBaqG5OB6Vv-BeYBlqvzAibfhzlwDyDKFOCMzDwRAwAAzwAAAFBO.png)
