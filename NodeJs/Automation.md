# Automation

---

## Puppeteer

```
const puppeteer = require('puppeteer');

function delay(timeout) {
  return new Promise((resolve) => {
    setTimeout(resolve, timeout);
  });
}

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('https://www.baidu.com');
  await page.screenshot({path: 'step1.png'});
  await page.evaluate(() => {
    $('button.loginButton').trigger('click');
  });
  await page.waitForSelector('#id_corpid');
  await page.evaluate(() => {
    $(".nav-tabs li:eq(1) a").trigger('click');
  });
  await delay(500);
  await page.evaluate(() => {
    $("#id_urs").val('username');
    $("#id_urspw").val('password');
  });
  await page.evaluate(() => {
    $(".tab-pane.active .btn ").trigger("click");
  });
  await delay(3000);
  await page.screenshot({path: 'step2.png'});
  await browser.close();
})();
```