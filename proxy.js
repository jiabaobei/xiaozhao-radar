// 校招雷达 · AnySearch CORS 本地代理（Node.js，10 行核心）
// 用法：node proxy.js   →   http://localhost:8787
// 校招雷达页面会自动检测本代理并优先使用（比公共代理稳定、无第三方中转）
// 想换端口：node proxy.js 9090
const http = require('http'), https = require('https'), { URL } = require('url');
const PORT = parseInt(process.argv[2] || '8787', 10);
http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', '*');
  if (req.method === 'OPTIONS') { res.writeHead(204); res.end(); return; }
  const target = new URL(decodeURIComponent(req.url.slice(1))); // /https://api.anysearch.com/mcp
  const isHttps = target.protocol === 'https:';
  const r = (isHttps ? https : http).request({
    hostname: target.hostname, path: target.pathname + target.search,
    method: req.method, headers: { ...req.headers, host: target.host, 'content-type': 'application/json' }
  }, x => { res.writeHead(x.statusCode, x.headers); x.pipe(res); });
  let b = ''; req.on('data', c => b += c); req.on('end', () => { if (b) r.write(b); r.end(); });
  r.on('error', () => { res.writeHead(502); res.end('proxy error'); });
}).listen(PORT, () => console.log('✅ AnySearch 代理已启动: http://localhost:' + PORT + '/ <目标URL>'));
