$dataFile = 'list.csv'
$imageDir = ''
$ext = ".jpg"
$batchsize = 10
$count = 0
$batch = 0

$pk1s = Import-Csv $dataFile -Delimiter '|'

ForEach ($pk1 in $pk1s) { 
    $count = $count + 1
    $dirname = 'user' + $pk1.id
    $filename = $pk1.username + $ext
    $dst = $dirname + "\" + $filename

    New-Item $dirname -ItemType Directory | Out-Null
    Copy-Item 'sample.jpg' -Destination $dst
    Compress-Archive -Path $dirname -Update -DestinationPath avatars.zip
    Remove-Item $dirname -Recurse

    # ✅ Fixed comparison operator from "=" to "-eq"
    If ($count -eq $batchsize) {
        $count = 0
        $batch = $batch + 1
        $batchzipname = "avatars_batch_" + $batch + ".zip"
        Rename-Item -Path avatars.zip -NewName $batchzipname 
    }
}

# Final batch wrap-up
$batch = $batch + 1
$avatarBatch = "avatars_batch_" + $batch + ".zip"
Rename-Item -Path avatars.zip -NewName $avatarBatch