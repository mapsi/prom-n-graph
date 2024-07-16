import express from "express";
import promClient from "prom-client";

const app = express();
const collectDefaultMetrics = promClient.collectDefaultMetrics;

// Collect default metrics
collectDefaultMetrics();

// Create a custom metric
const httpRequestsTotal = new promClient.Counter({
  name: "http_requests_total",
  help: "Total number of HTTP requests",
  labelNames: ["method", "path"],
});

app.get("/", (req, res) => {
  // Increment the custom metric
  httpRequestsTotal.inc({ method: req.method, path: req.path });

  res.send("Hello World");
});

app.get("/metrics", async (req, res) => {
  res.set("Content-Type", promClient.register.contentType);
  res.end(await promClient.register.metrics());
});

app.listen(3000, () => console.log("Server is running on port 3000"));
