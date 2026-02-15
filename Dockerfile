FROM python:3.12-slim

WORKDIR /app

COPY All_Diets.csv .
COPY data_analysis.py .

RUN pip install pandas matplotlib seaborn

CMD ["python", "data_analysis.py"]
