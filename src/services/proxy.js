const http = require("http");
const https = require("https");
const { URL } = require("url");

function fetchRemote(rawUrl) {
  const parsed = new URL(rawUrl);
  const client = parsed.protocol === "http:" ? http : https;

  return new Promise((resolve, reject) => {
    const req = client.request(
      {
        hostname: parsed.hostname,
        port: parsed.port || (parsed.protocol === "http:" ? 80 : 443),
        path: parsed.pathname + (parsed.search || ""),
        method: "GET",
      },
      (res) => {
        const chunks = [];
        res.on("data", (d) => chunks.push(d));
        res.on("end", () => {
          resolve({
            statusCode: res.statusCode,
            headers: res.headers,
            body: Buffer.concat(chunks).toString("utf8"),
          });
        });
      }
    );
    req.on("error", reject);
    req.end();
  });
}

async function proxyHandler(req, res) {
  const target = req.query.url;
  if (!target) {
    res.status(400).json({ error: "missing url" });
    return;
  }

  try {
    const result = await fetchRemote(target);
    res
      .status(result.statusCode || 200)
      .set(result.headers || {})
      .send(result.body);
  } catch (err) {
    res.status(502).json({ error: "upstream error", detail: String(err && err.message || err) });
  }
}

module.exports = { proxyHandler, fetchRemote };
