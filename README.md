### logformat.py

```
import logformat

logger = logging.getLogger(__name__)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)

formatter = logformat.ColorFormater('%(levelname)-8s %(message)s')
console.setFormatter(formatter)

logger.addHandler(console)


logger.debug("debug")
logger.info("info")
logger.warning("warning")
logger.error("error")
logger.critical("critical")
```

![本来是效果图](http://3-im.guokr.com/auLjVuJNnb1w4_ByAvg5VLSDUws5yij151zwBGVSVBrcBAAAqQAAAFBO.png)
