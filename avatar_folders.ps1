$dataFile = 'list.csv'
# this assumes a "|" delimited file where the PK1 value (eg. _123_1) is the first column and the file identifier is the 2nd.

$imageDir = ''
# path to the image source

$ext = ".jpg"

$batchsize = 10
$count = 0
$batch = 0






$pk1s = Import-Csv list.csv -Delimiter '|'
 
ForEach ($pk1 in $pk1s) { 

 $count = $count + 1
 $dirname = 'user' + $pk1.id
 $filename = $pk1.username + $ext
 $dst = $dirname + "\" + $filename
 New-Item $dirname -type directory
 Copy-Item 'sample.jpg' -Destination $dst
 Compress-Archive -Path $dirname -Update -DestinationPath avatars.zip
 Remove-Item $dirname -Recurse
 If ($count = $batchsize) {
   $count = 0
   $batch = $batch + 1
   $batchzipname = "avatars_batch_" + $batch + ".zip"
   Rename-Item -Path avatars.zip -NewName $batchzipname 
 }
}

$batch = $batch + 1
$avatarBatch = "avatars_batch_" + $batch + ".zip"
Rename-Item -Path avatars.zip -NewName $avatarBatch