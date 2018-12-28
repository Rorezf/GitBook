# Utils

## Excel

```php
include './testlink/lib/excel/PHPExcel/IOFactory.php';
$tmp_name = $_FILES["xls"]["tmp_name"];
$name = $_FILES["xls"]["name"];
$inputFileName = "D:/Google/$name";
move_uploaded_file($tmp_name, $inputFileName);

$inputFileType = PHPExcel_IOFactory::identify($inputFileName);
$objReader = PHPExcel_IOFactory::createReader($inputFileType);

$worksheetNames = $objReader->listWorksheetNames($inputFileName);
var_dump($worksheetNames[0]);

$objPHPExcel = $objReader->load($inputFileName);
$sheet = $objPHPExcel->getSheet(0);
$highestRow = $sheet->getHighestRow();
$highestColumn = $sheet->getHighestColumn();
for ($row = 1; $row <= $highestRow; $row++){
    $rowData = $sheet->rangeToArray('A' . $row . ':' . $highestColumn . $row, NULL, TRUE, FALSE);
    var_dump($rowData);
    echo "<br>";
}
unlink($inputFileName);
```

