# Stage 1: Build environment (install dependencies and prepare app)
FROM python:3.12-slim AS builder

WORKDIR /app

# Copy only what is needed for the analysis
COPY ALL_Diets.csv .
COPY data_analysis.py .

# Install Python dependencies
RUN pip install --no-cache-dir pandas matplotlib seaborn

# Stage 2: Runtime image (minimal)
FROM python:3.12-slim

WORKDIR /app

# Copy only the files and installed packages from the builder stage
COPY --from=builder /app /app

# Set the default command to run the analysis
CMD ["python", "data_analysis.py"]
