async function proxy(req, res) {
    const url = req.query.url;
    if (!url) return res.status(400).json({ error: "missing url" });
  
    try {
      const r = await fetch(url);
      const body = await r.text();
      res.status(r.status || 200).send(body);
    } catch (e) {
      res.status(502).json({ error: "upstream error" });
    }
  }
  
  module.exports = { proxy };
  