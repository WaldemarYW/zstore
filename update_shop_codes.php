<?php

require_once 'init.php';

// Скрипт для первинної/примусової нумерації всіх товарів у магазині (1, 2, 3...)
$force = isset($_GET['force']) || (php_sapi_name() === 'cli');
$count = \App\Entity\Item::reindexShopCodes(true);

header('Content-Type: text/plain; charset=utf-8');
echo "OK. Успішно пронумеровано {$count} товарів по порядку (1, 2, 3...).";
