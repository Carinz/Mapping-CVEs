from asyncore import write

response = b'<!doctype html>\n<html>\n  <head>\n    <meta data-n-head="1" charset="utf-8"><meta data-n-head="1" name="viewport" \
content="width=device-width,initial-scale=1"><meta data-n-head="1" data-hid="description" name="description" \
content=""><title>Argilla</title><link data-n-head="1" rel="icon" type="image/x-icon" href="favicon.ico"><link \
data-n-head="1" rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png"><link data-n-head="1" rel="icon" \
sizes="32x32" href="favicon-32x32.png"><link data-n-head="1" rel="icon" sizes="16x16" href="favicon-16x16.png"><link \
data-n-head="1" rel="manifest" href="site.webmanifest"><base href="/"><link rel="preload" href="/_nuxt/1f8eea4.js" \
as="script"><link rel="preload" href="/_nuxt/4c23abf.js" as="script"><link rel="preload" href="/_nuxt/ac16c1e.js" \
as="script"><link rel="preload" href="/_nuxt/7ba2266.js" as="script">\n  </head>\n  <body>\n    <div \
id="__nuxt"><style>#nuxt-loading{background:#fff;visibility:hidden;opacity:0;position:absolute;left:0;right:0;top:0;bott\
om:0;display:flex;justify-content:center;align-items:center;flex-direction:column;animation:nuxtLoadingIn 10s \
ease;-webkit-animation:nuxtLoadingIn 10s ease;animation-fill-mode:forwards;overflow:hidden}@keyframes \
nuxtLoadingIn{0%{visibility:hidden;opacity:0}20%{visibility:visible;opacity:0}100%{visibility:visible;opacity:1}}@-webki\
t-keyframes \
nuxtLoadingIn{0%{visibility:hidden;opacity:0}20%{visibility:visible;opacity:0}100%{visibility:visible;opacity:1}}#nuxt-l\
oading>div,#nuxt-loading>div:after{border-radius:50%;width:5rem;height:5rem}#nuxt-loading>div{font-size:10px;position:re\
lative;text-indent:-9999em;border:.5rem solid #f5f5f5;border-left:.5rem solid \
#d3d3d3;-webkit-transform:translateZ(0);-ms-transform:translateZ(0);transform:translateZ(0);-webkit-animation:nuxtLoadin\
g 1.1s infinite linear;animation:nuxtLoading 1.1s infinite linear}#nuxt-loading.error>div{border-left:.5rem solid \
#ff4500;animation-duration:5s}@-webkit-keyframes \
nuxtLoading{0%{-webkit-transform:rotate(0);transform:rotate(0)}100%{-webkit-transform:rotate(360deg);transform:rotate(36\
0deg)}}@keyframes \
nuxtLoading{0%{-webkit-transform:rotate(0);transform:rotate(0)}100%{-webkit-transform:rotate(360deg);transform:rotate(36\
0deg)}}</style> <script>window.addEventListener("error",(function(){var \
e=document.getElementById("nuxt-loading");e&&(e.className+=" error")}))</script> <div id="nuxt-loading" \
aria-live="polite" role="status"><div>Loading...</div></div> \
</div><script>window.__NUXT__={config:{clientVersion:"2.1.0",documentationSite:"https://docs.argilla.io/",documentationP\
ersistentStorage:"https://docs.argilla.io/latest/getting_started/how-to-configure-argilla-on-huggingface/#persistent-sto\
rage",_app:{basePath:"/",assetsPath:"/_nuxt/",cdnURL:null}}}</script>\n  <script \
src="/_nuxt/1f8eea4.js"></script><script src="/_nuxt/4c23abf.js"></script><script \
src="/_nuxt/ac16c1e.js"></script><script src="/_nuxt/7ba2266.js"></script></body>\n</html>\n'

with open('response.html', 'wb') as f:
    f.write(response)