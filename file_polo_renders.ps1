$src = 'C:\Users\maxim\Downloads\Golf Polo renders'
$dst = 'G:\My Drive\Claude stuff\Wardrobe Photos\Retail'
$map = [ordered]@{
  '51' = 'tops_51_tikeden-navy-toucan-polo'
  '52' = 'tops_52_peter-millar-white-rsgc-polo'
  '53' = 'tops_53_fairway-greene-white-interclub-polo'
  '54' = 'tops_54_fairway-greene-pink-rsgc-polo'
  '55' = 'tops_55_cross-taupe-diamond-polo'
  '56' = 'tops_56_puma-lime-stripe-polo'
  '57' = 'tops_57_peter-millar-periwinkle-rsgc-polo'
  '58' = 'tops_58_navy-jacquard-rsgc-polo'
  '59' = 'tops_59_ping-blue-colourblock-polo'
  '60' = 'tops_60_footjoy-grey-mint-floral-rsgc-polo'
}
foreach ($k in $map.Keys) {
  $from = Join-Path $src ($k + '.jpeg')
  $to   = Join-Path $dst ($map[$k] + '_retail.jpeg')
  Copy-Item -LiteralPath $from -Destination $to -Force
  $fi = Get-Item -LiteralPath $to
  Write-Output ("OK  " + $fi.Name + "  " + [math]::Round($fi.Length/1KB) + " KB")
}
