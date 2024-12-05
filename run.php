<?php
$command = escapeshellcmd('/usr/bin/python3 /Applications/AMPPS/www/music_ocr/app.py');
$output = shell_exec($command);
echo $output;
?>
