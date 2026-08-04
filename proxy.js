// 校招雷达 · 本地 CORS 代理（Node.js，10 行核心）
// 用法：node proxy.js   →   http://localhost:8787
// 用途：
//  1) AnySearch 兜底：页面自动检测本代理优先使用（比公共代理稳定、无第三方中转）
//  2) 腾讯文档最终兜底：转发 docs.qq.com 数据接口并加 CORS 头（匿名可读）
// 想换端口：node proxy.js 9090
const http = require('http'), https = require('https'), { URL } = require('url');
const PORT = parseInt(process.argv[2] || '8787', 10);
http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', '*');
  if (req.method === 'OPTIONS') { res.writeHead(204); res.end(); return; }
  try {
    const target = new URL(decodeURIComponent(req.url.slice(1))); // /https://api.anysearch.com/mcp
    const isHttps = target.protocol === 'https:';
    // 只透传必要头：Accept / Content-Type / Authorization（AnySearch 需要）；其余浏览器噪音头一律不转发，
    // 避免 docs.qq.com 因 Origin/Sec-Fetch/Accept-Language 等差异返回 401
    const headers = {
      host: target.host,
      accept: 'application/json, text/plain, */*',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    };
    if (req.headers['content-type']) headers['content-type'] = req.headers['content-type'];
    if (req.headers['authorization']) headers['authorization'] = req.headers['authorization'];
    if (req.headers['x-anysearch-client']) headers['x-anysearch-client'] = req.headers['x-anysearch-client'];
    // 浏览器 fetch 无法设置 Referer，这里按目标站强制注入（docs.qq.com 校验 Referer，缺失会 401）
    if (target.hostname === 'docs.qq.com' && !headers.referer) {
      headers.referer = 'https://docs.qq.com/smartsheet/DTkRMUVhoUWJXZEhJ';
    }
    const r = (isHttps ? https : http).request({
      hostname: target.hostname, port: target.port, path: target.pathname + target.search,
      method: req.method, headers
    }, x => { res.writeHead(x.statusCode, x.headers); x.pipe(res); });
    let b = ''; req.on('data', c => b += c); req.on('end', () => { if (b) r.write(b); r.end(); });
    r.on('error', e => { res.writeHead(502); res.end('proxy error: ' + e.message); });
  } catch (e) {
    res.writeHead(400); res.end('bad target: ' + e.message);
  }
}).listen(PORT, () => console.log('✅ 本地代理已启动: http://localhost:' + PORT + '/ <目标URL>'));
