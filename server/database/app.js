const express = require("express");
const mongoose = require("mongoose");
const fs = require("fs");
const path = require("path");
const cors = require("cors");

const app = express();
const port = Number(process.env.PORT || 3030);
app.use(cors());
app.use(express.json({ limit: "1mb" }));
app.use(express.urlencoded({ extended: false }));

function readSeedFile(filename) {
  const candidates = [
    path.join(__dirname, "data", filename),
    path.join(__dirname, filename)
  ];
  const filePath = candidates.find((candidate) => fs.existsSync(candidate));
  if (!filePath) throw new Error(`Seed file not found: ${filename}`);
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

const reviewsData = readSeedFile("reviews.json");
const dealershipsData = readSeedFile("dealerships.json");

const Reviews = require("./review");
const Dealerships = require("./dealership");

app.get("/", (_req, res) => {
  res.send("Welcome to the Mongoose API");
});

app.get("/fetchReviews", async (_req, res) => {
  try {
    const documents = await Reviews.find().sort({ id: 1 }).lean();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: "Error fetching reviews" });
  }
});

app.get("/fetchReviews/dealer/:id", async (req, res) => {
  try {
    const dealerId = Number(req.params.id);
    if (!Number.isInteger(dealerId)) {
      return res.status(400).json({ error: "Dealer ID must be a number" });
    }
    const documents = await Reviews.find({ dealership: dealerId }).sort({ id: 1 }).lean();
    return res.json(documents);
  } catch (error) {
    return res.status(500).json({ error: "Error fetching dealer reviews" });
  }
});

app.get("/fetchDealers", async (_req, res) => {
  try {
    const documents = await Dealerships.find({}).sort({ id: 1 }).lean();
    return res.json(documents);
  } catch (error) {
    return res.status(500).json({ error: "Error fetching dealerships" });
  }
});

app.get("/fetchDealers/:state", async (req, res) => {
  try {
    const state = req.params.state;
    const filter = state.toLowerCase() === "all"
      ? {}
      : { state: new RegExp("^" + state.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "$", "i") };
    const documents = await Dealerships.find(filter).sort({ id: 1 }).lean();
    return res.json(documents);
  } catch (error) {
    return res.status(500).json({ error: "Error fetching dealerships by state" });
  }
});

app.get("/fetchDealer/:id", async (req, res) => {
  try {
    const dealerId = Number(req.params.id);
    if (!Number.isInteger(dealerId)) {
      return res.status(400).json({ error: "Dealer ID must be a number" });
    }
    const document = await Dealerships.findOne({ id: dealerId }).lean();
    if (!document) return res.status(404).json({ error: "Dealer not found" });
    return res.json([document]);
  } catch (error) {
    return res.status(500).json({ error: "Error fetching dealer" });
  }
});

app.post("/insert_review", async (req, res) => {
  try {
    const data = req.body;
    const required = [
      "name", "dealership", "review", "purchase",
      "purchase_date", "car_make", "car_model", "car_year"
    ];
    const missing = required.filter((field) => data?.[field] === undefined);
    if (missing.length) {
      return res.status(400).json({ error: "Missing fields: " + missing.join(", ") });
    }
    const latest = await Reviews.findOne().sort({ id: -1 }).lean();
    const newId = latest ? latest.id + 1 : 1;
    const review = new Reviews({
      id: newId,
      name: String(data.name),
      dealership: Number(data.dealership),
      review: String(data.review),
      purchase: Boolean(data.purchase),
      purchase_date: String(data.purchase_date),
      car_make: String(data.car_make),
      car_model: String(data.car_model),
      car_year: Number(data.car_year)
    });
    const savedReview = await review.save();
    return res.status(201).json(savedReview);
  } catch (error) {
    console.error("Error inserting review:", error);
    return res.status(500).json({ error: "Error inserting review" });
  }
});

async function start() {
  const mongoUrl = process.env.MONGODB_URL || "mongodb://mongo_db:27017/";
  await mongoose.connect(mongoUrl, { dbName: "dealershipsDB" });

  await Reviews.deleteMany({});
  await Reviews.insertMany(reviewsData.reviews);
  await Dealerships.deleteMany({});
  await Dealerships.insertMany(dealershipsData.dealerships);

  app.listen(port, "0.0.0.0", () => {
    console.log(`Server is running on port ${port}`);
  });
}

start().catch((error) => {
  console.error("Unable to start dealership API:", error);
  process.exit(1);
});
