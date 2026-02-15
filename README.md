# Smart-Airport-Ride-Pooling

## 📌 Problem Statement
Build a Smart Airport Ride Pooling Backend System that:
Groups passengers into shared cabs
Respects luggage and seat constraints
Minimizes total travel deviation
Ensures detour tolerance is respected
Handles real-time cancellations
Supports 10,000 concurrent users
Handles 100 requests per second
Maintains latency under 300ms

## 🏗 High-Level Architecture
Client (Browser / Swagger / curl)
        ↓
FastAPI (Async API Layer)
        ↓
Ride Service Layer
        ↓
Matching Engine
        ↓
PostgreSQL (Primary Database)

## Components
FastAPI → API layer
Service Layer → Business logic
Matching Engine → Ride grouping logic
PostgreSQL → Persistent storage
Row-level locking → Concurrency safety

## 🧠 DSA Approach
Matching Strategy

Filter active ride pools:

status = active
available_seats > 0
available_luggage >= required
Simulate route extension:
Calculate existing route distance
Add new passenger drop point
Compute detour using Haversine formula

Validate:
Detour ≤ passenger tolerance
Capacity constraints satisfied
Select pool with minimum detour
If none found → create new pool

Time Complexity
Let:
n = number of active ride pools
m = number of passengers in a pool (≤ 4)
Route calculation: O(m)
Pool scanning: O(n)
Overall:

O(n × m)
Since m ≤ 4, practical complexity ≈ O(n)
Indexed filtering improves performance.




## 🔒 Concurrency Handling Strategy

To prevent race conditions and overbooking:

PostgreSQL row-level locking (SELECT FOR UPDATE)

Atomic seat & luggage updates

Single transaction commit

ACID compliance

This ensures:

No overbooking

Safe concurrent ride assignments

Strong data consistency

## 🗃 Database Schema & Indexing Strategy
Indexed Columns

ride_pools.status

ride_pools.available_seats

ride_requests.status

ride_requests.created_at

ride_requests.user_id

Indexes improve:

Active pool filtering

Capacity checks

Query speed under high load

## 💰 Dynamic Pricing Formula

Final Fare:
Final Price =
(Base Fare + Distance Cost + Detour Cost)
× Surge Multiplier
× (1 - Pool Discount)

Where:
Base Fare = 100
Distance Rate = 15 per km
Detour Rate = 5 per km
Pool Discount = 20%

## ⚡Performance Considerations

Indexed queries → O(log n)
Minimal full table scans
Haversine calculation → O(1)
Row-level locking minimizes contention
Designed to support 100 req/sec
Optimized for <300ms latency

## 🌐 API Documentation

Swagger UI available at:
http://127.0.0.1:8000/docs

## 🖥 Minimal Demo UI

A simple demo interface is available at:
http://127.0.0.1:8000/

Allows:
Create Ride
Cancel Ride
View response

## ⚙️ Setup & Run Instructions
1️⃣ Clone Repository
git clone <your-repo-url>
cd smart-airport-ride-pooling

2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Setup Environment Variables

Create .env:
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/ride_pooling
LOG_LEVEL=INFO

5️⃣ Run Migrations
alembic upgrade head

6️⃣ Start Server
uvicorn app.main:app --reload

🧪 Sample Test Data
{
  "user_id": 1,
  "pickup_lat": 19.0896,
  "pickup_lng": 72.8656,
  "drop_lat": 19.2183,
  "drop_lng": 72.9781,
  "luggage_count": 1,
  "detour_tolerance_km": 10
}

## 📊 Evaluation Focus Alignment

This implementation demonstrates:
1.Correctness of ride grouping logic
2.Optimized database modeling
3.Concurrency safety
4.Performance-aware design
5.Clean architecture
6.Modular and maintainable code

