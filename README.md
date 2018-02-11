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
logging.error("error")
logging.critical("critical")
```

![本来是效果图](http://3-im.guokr.com/auLjVuJNnb1w4_ByAvg5VLSDUws5yij151zwBGVSVBrcBAAAqQAAAFBO.png)
