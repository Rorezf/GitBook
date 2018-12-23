# Excel

## Write

### xlwt

```text
def customStyle(self,label):
    custom = xlwt.XFStyle()
    custom.alignment.horz = 1
    custom.alignment.vert = 1
    custom.alignment.wrap = 1 

    font = xlwt.Font()
    font.height = 210
    custom.font = font

    borders = xlwt.Borders()
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN
    custom.borders = borders

    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    if label == 'cell':
        pattern.pattern_fore_colour = 82
    elif label == 'head':
        pattern.pattern_fore_colour = 3
    elif label == 'bug':
        pattern.pattern_fore_colour = 29
    custom.pattern = pattern
    return custom

self.style = self.customStyle('cell')
self.book = xlwt.Workbook()
self.sheet = self.book.add_sheet(self.subject.split("-")[0])
self.sheet.col(0).width = 4000
for i in [1,8,10,11]:
    self.sheet.col(i).width = 10000
self.sheet.write(1, 0, "Summary", self.styleHead)
self.sheet.write_merge(rowCount,rowCount + spanNum - 1, 0, 0, key, self.style)
self.book.save(self.xlsTemp)
```

