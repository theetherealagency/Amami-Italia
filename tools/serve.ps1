# No-store static server for src/, for Windows machines without Python.
# Same job as tools/serve.py:  powershell -File tools/serve.ps1 8765 src
param([int]$Port = 8765, [string]$Root = 'src')
$Root = (Resolve-Path $Root).Path
$types = @{ '.html'='text/html; charset=utf-8'; '.css'='text/css; charset=utf-8'; '.js'='text/javascript; charset=utf-8';
  '.json'='application/json'; '.xml'='application/xml'; '.svg'='image/svg+xml'; '.png'='image/png'; '.jpg'='image/jpeg';
  '.jpeg'='image/jpeg'; '.webp'='image/webp'; '.gif'='image/gif'; '.ico'='image/x-icon'; '.mp4'='video/mp4';
  '.woff2'='font/woff2'; '.woff'='font/woff'; '.txt'='text/plain; charset=utf-8'; '.pdf'='application/pdf' }
$listener = New-Object Net.HttpListener
$listener.Prefixes.Add("http://localhost:$Port/")
$listener.Start()
Write-Host "Serving $Root on http://localhost:$Port/"
while ($listener.IsListening) {
  $ctx = $listener.GetContext(); $res = $ctx.Response
  try {
    $rel = [Uri]::UnescapeDataString($ctx.Request.Url.AbsolutePath).TrimStart('/').Replace('/', '\')
    $path = Join-Path $Root $rel
    if ((Test-Path $path -PathType Container)) {
      if (-not $ctx.Request.Url.AbsolutePath.EndsWith('/')) { $res.StatusCode = 308; $res.RedirectLocation = $ctx.Request.Url.AbsolutePath + '/'; $res.Close(); continue }
      $path = Join-Path $path 'index.html'
    }
    if (-not $path.StartsWith($Root) -or -not (Test-Path $path -PathType Leaf)) {
      $res.StatusCode = 404; $path = Join-Path $Root '404\index.html'
    }
    $bytes = [IO.File]::ReadAllBytes($path)
    $ext = [IO.Path]::GetExtension($path).ToLower()
    $res.ContentType = $(if ($types[$ext]) { $types[$ext] } else { 'application/octet-stream' })
    $res.Headers.Add('Cache-Control', 'no-store')
    $res.ContentLength64 = $bytes.Length
    if ($ctx.Request.HttpMethod -ne 'HEAD') { $res.OutputStream.Write($bytes, 0, $bytes.Length) }
  } catch { try { $res.StatusCode = 500 } catch {} }
  finally { try { $res.Close() } catch {} }
}
